# -*- coding: utf-8 -*-
import sys, os
import mainwindow as mainwindow
import usb.core

from PyQt5 import *
import itertools
import json

import liquidctl.util
from liquidctl.driver.kraken_two import KrakenTwoDriver
from liquidctl.driver.nzxt_smart_device import NzxtSmartDeviceDriver

from liquidctl.common.preset import DeviceLightingPreset
from liquidctl.common.qringwidget import QRingWidget

DRIVERS = [
    KrakenTwoDriver,
    NzxtSmartDeviceDriver,
]
_SLICE_BORDER = {
    'enable'  : QtGui.QColor(1,1,1,160),
    'disable' : QtGui.QColor(127,127,127,160),
    'picked'  : QtGui.QPalette().color(QtGui.QPalette.HighlightedText)
}

_channels = ['logo', 'ring', 'sync']
_attributes = ['channel', 'mode', 'colors', 'speed']

def find_all_supported_devices():
    res = map(lambda driver: driver.find_supported_devices(), DRIVERS)
    return itertools.chain(*res)

class MainWindow(QtWidgets.QMainWindow):

    def menu_file_save(self):
        pass

    def menu_device_reload(self):
        """Populates device menu with supported devices"""
        last_device = self.device if hasattr(self, 'device') else None

        self.devices = list(enumerate(find_all_supported_devices()))
        if len(self.devices) == 0:
            return

        self.ui.menu_Select_Device.clear()

        for i, dev in self.devices:
            action = QtWidgets.QAction(dev.description, self.ui.menu_Select_Device)
            action.setObjectName(dev.device.serial_number)
            action.setCheckable(True)
            action.triggered.connect(self.menu_device_selected)

            self.ui.menu_Select_Device.addAction(action)

            if ((last_device == None) or (last_device.device.serial_number == dev.device.serial_number)):
                self.device = dev

        self.light_device_selected()
    def menu_device_selected(self):
        """Activates device menu item when clicked"""
        for i, dev in self.devices:
            if (dev.device.serial_number == self.sender().objectName()):
                self.device = dev
                break

        self.light_device_selected()

    def light_preset_highlight_valid_slices(self):
        """Highlights ring segments and radiobuttons that are valid for the preset"""
        mode = self.get_ui_value_of_preset_attr('mode')
        if mode == '':
            mode = self.ui.labelRingMode.text().lower()
            if mode == '':
                return

        mval, mod2, mod4, mincolors, maxcolors, ringonly = self.device.get_color_modes()[mode]
                    
        for i, ps in enumerate(self.widget.slices()):
            ps.setBorderColor(_SLICE_BORDER['enable'])

        for i, ps in enumerate(self.widget.slices()):
            if i == maxcolors:
                break
            ps.setBorderColor(_SLICE_BORDER['disable'])
        
        if isinstance(self.picked, QtChart.QPieSlice):
            self.picked.setBorderColor(_SLICE_BORDER['picked'])
        
        font = self.ui.labelLogo.font()
        font.setUnderline(self.picked == self.ui.labelLogo)
        self.ui.labelLogo.setFont(font)
    
    def update_animation_speed_label(self, value: str):
        """Updates animation speed information"""
        speed = self.get_ui_value_of_preset_attr('speed')
        self.ui.labelPresetAniSpeedLabel.setText("Animation Speed: %s" % speed.title())
    def get_animation_speed_name(self, speed):
        for key, value in self.device.get_animation_speeds().items():
            if (value == speed):
                return key

    def light_device_selected(self):
        """Updates the interface when a device has been selected"""
        for item in self.ui.menu_Select_Device.children():
            if isinstance(item, QtWidgets.QAction):
                item.setChecked((self.device.device.serial_number == item.objectName()))

        self.ui.comboBoxPresetModes.clear()

        for mode in self.device.get_color_modes():
            self.ui.comboBoxPresetModes.addItem(str(mode).title())

        self.ui.labelDevDeviceName.setText("Device: %s" % self.device.description)
        self.ui.labelDevSerialNo.setText("Serial No: %s" % self.device.device.serial_number)

        self.light_preset_highlight_valid_slices()

        if (hasattr(self, 'preset')):
            channel = self.get_ui_value_of_preset_attr('channel')
            self.update_ui_from_preset(self.preset[channel])

    def preset_save(self):
        """saves values to preset based on currenly selected channel"""
        if (self.device == None):
            return
        
        current_channel = self.get_ui_value_of_preset_attr('channel')

        self.updating = (current_channel == 'sync') # allow all labels to update when sync, otherwise they update later
        self.preset[current_channel].values = self.update_preset_from_ui(current_channel)

        if (current_channel == 'sync'):
            self.preset['ring'].values = self.preset[current_channel].values
            self.preset['logo'].values = self.preset[current_channel].values

        for channel in _channels:
            self.preset[channel].colors = self.preset[current_channel].colors

        self.preset['logo'].write()
        self.preset['ring'].write()

        self.updating = True
        self.update_ui_from_preset(self.preset[current_channel])
    
    def preset_file_import(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Import Lighting Preset", "","NZXQT Lighting JSON Profile(*.json)", options=options)
        if fileName:
            self.settings_load(fileName)
    def preset_file_export(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None,"Export Lighting Preset","","NZXQT Lighting JSON Profile(*.json)", options=options)

        if fileName:
            presets = {}

            for channel in ['logo', 'ring']:
                data = {}
                for attr in ['mode', 'colors', 'speed']:
                    value = self.preset[channel].attr(attr)
                    if (attr == 'colors'):
                        if (channel == 'logo'):
                            value = []
                        else:
                            value = list(map(lambda x: x.hex(), value))
                    data[attr] = value
                presets[channel] = data

            with open(fileName, "w") as file:
                json.dump(presets, file, sort_keys=True, indent=4)
        
    def get_logo_qcolor(self) -> QtGui.QColor:
        """Gets the logo QColor from its Palette"""
        return self.ui.labelLogo.palette().color(0)
    def both_selected(self):
        """Reselects both preset when radiobutton is activated"""
        self.update_ui_from_preset(self.preset['sync'])
    def logo_selected(self, data):
        """Reselects logo preset when radiobutton is activated"""
        self.picked = self.ui.labelLogo

        self.colorDialog.setCurrentColor(self.get_logo_qcolor())
        self.update_ui_from_preset(self.preset['logo'])
    def ring_selected(self):
        """Reselects ring preset when radiobutton is activated"""
        self.last_color = self.last_slice.color()
        self.set_picked_slice(self.last_slice)
        self.update_ui_from_preset(self.preset['ring'])
    
    def ring_widget_init(self):
        """Adds a ring widget as a QChart"""
        self.widget = QRingWidget(self.ui.frameLightingWidget)
        self.widget.setBackgroundColor(self.ui.tab_2_1.palette().color(4))
        
        self.widget.slice_clicked.connect(self.ring_widget_slice_clicked)
        self.widget.slice_hovered.connect(self.ring_widget_slice_hovered)
        self.widget.slice_dblclicked.connect(self.ring_widget_slice_dblclicked)

        self.last_slice = self.widget.slices()[0]
        self.picked = self.last_slice

    def ring_widget_slice_clicked(self, pieslice):
        """Stores slice and sets color dialog color"""
        self.set_picked_slice(pieslice)
    def ring_widget_slice_dblclicked(self):
        """Fills all slices with the same color"""
        for i, ps in enumerate(self.widget.slices()):
            ps.setColor(self.last_color)
        self.check_revert_state()
    def ring_widget_slice_hovered(self, pieslice, state):
        """Event when slice is hovered"""
        if state:
            self.last_color = pieslice.color()

        self.light_preset_highlight_valid_slices()

    def set_picked_slice(self, pieslice):
        """store the picked slice object"""
        self.picked = pieslice
        self.last_slice = pieslice

        # we do not set colors 
        for attr in ['channel', 'mode', 'speed']:
            self.set_ui_value_to_preset_attr(self.preset['ring'], attr)
        self.colorDialog.setCurrentColor(self.last_color)
        self.light_preset_highlight_valid_slices()
    
    def color_dialog_closing(self, evt):
        """ captures the event that would otherwise cause the colordialog to disappear """
        pass
    def color_dialog_changed(self, value):
        """Updates color on selected element"""
        if isinstance(self.picked, QtWidgets.QLabel):
            palette = QtGui.QPalette()
            palette.setColor(self.ui.labelLogo.foregroundRole(), value)
            self.ui.labelLogo.setPalette(palette)
        elif isinstance(self.picked, QtChart.QPieSlice):
            self.picked.setColor(value)
        self.check_revert_state()
    def color_dialog_init(self):
        """ creates a color dialog and adds it to a widget on the window """
        self.colorDialog = QtWidgets.QColorDialog()
        self.colorDialog.setOptions(QtWidgets.QColorDialog.NoButtons)
        self.colorDialog.currentColorChanged.connect(self.color_dialog_changed)
        self.colorDialog.done = self.color_dialog_closing
        window = self.ui.mdiArea.addSubWindow(self.colorDialog, flags=QtCore.Qt.FramelessWindowHint)
        window.showMaximized()

    def check_revert_state(self):
        """ compares user-interface values to those in the preset, returns TRUE if they match, FALSE if they differ"""
        revert = False
        channel = self.get_ui_value_of_preset_attr('channel')

        for attr in _attributes:
            if (attr == 'channel'):
                continue

            if (self.get_ui_value_of_preset_attr(attr) != self.preset[channel].attr(attr)):
                revert = True
                break

        self.ui.labelPresetRevert.setEnabled(revert)
    def revert_color_state(self, evt):
        """ restores the color chart values on the user-interface from those in the current channels preset """
        current_channel = self.get_ui_value_of_preset_attr('channel')

        for channel in _channels:
            for attr in _attributes:
                if (attr == 'channel'):
                   continue
                self.set_ui_value_to_preset_attr(self.preset[channel], attr)

        self.update_ui_from_preset(self.preset[current_channel])

        if (isinstance(self.picked, QtChart.QPieSlice)):
            color = self.picked.color()
        else:
            color = self.get_logo_qcolor()

        self.colorDialog.setCurrentColor(color)

    def update_preset_from_ui(self, channel = 'sync'):
        """returns a list in Preset format based on UI values"""
        return list(map(self.get_ui_value_of_preset_attr,_attributes))
    def update_ui_from_preset(self, preset: DeviceLightingPreset):
        """ updates ui values for the given preset data """
        current_channel = self.get_ui_value_of_preset_attr('channel')

        for attr in _attributes:
            if ((current_channel == preset.channel) and (attr == 'colors')):
                continue
            self.set_ui_value_to_preset_attr(preset, attr)

        self.check_revert_state()

    def get_ui_value_of_preset_attr(self, attr):
        """ returns the user-interface value for an attribute """
        if (attr == 'channel'):
            if ( self.ui.radioButtonPresetLogo.isChecked() ):
                return 'logo'
            if ( self.ui.radioButtonPresetRing.isChecked() ):
                return 'ring'
            if ( self.ui.radioButtonPresetBoth.isChecked() ):
                return 'sync'

        if (attr == 'mode'):
            return self.ui.comboBoxPresetModes.currentText().lower()

        if (attr == 'colors'):
            colors = [bytes.fromhex(self.get_logo_qcolor().name().strip("#"))]
            for i, ps in enumerate(self.widget.slices()):
                color = self.widget.slices()[index].color().name().strip("#")
                colors.append(bytes.fromhex(color))
            return colors

        if (attr == 'speed'):
            return self.get_animation_speed_name(self.ui.horizontalSliderASpeed.value())
    def set_ui_value_to_preset_attr(self, preset, attr):
        if (not isinstance(preset, DeviceLightingPreset)):
            raise TypeError("The object is not of type DeviceLightingPreset")
            
        if (not self.updating):
            return

        if (preset.channel == 'logo'):
            label = self.ui.labelLogoMode
            radio = self.ui.radioButtonPresetLogo
        elif (preset.channel == 'ring'):
            label = self.ui.labelRingMode
            radio = self.ui.radioButtonPresetRing
        else:
            label = self.ui.labelBothMode
            radio = self.ui.radioButtonPresetBoth

        if (attr == 'channel'):
            radio.setChecked(True)

        if (attr == 'mode'):
            mode = getattr(preset, attr).title()
            self.ui.comboBoxPresetModes.setCurrentText(mode)

            if (preset.channel in _channels):
                label.setText(mode)

            if (self.preset['ring'].mode == self.preset['logo'].mode):
                self.preset['sync'].mode = mode
                self.ui.labelBothMode.setText(mode)
            else:
                self.ui.labelBothMode.setText("Mixed-modes")

        if (attr == 'speed'):
            if (preset.speed not in preset.speeds):
                return
            self.ui.horizontalSliderASpeed.setValue(preset.speeds[preset.speed])
        
        if (attr == 'colors'):
            if (preset.channel == 'logo'):
                color = QtGui.QColor("#%s" % preset.colors[0].hex())
                palette = self.ui.labelLogo.palette()
                palette.setColor(0, color)
                self.ui.labelLogo.setPalette(palette)
            if (preset.channel == 'ring'):
                for i, ps in enumerate(self.widget.slices()):
                    if (i >= (len(preset.colors) - 1)):
                        break
                    ps.setColor(QtGui.QColor("#" + preset.colors[i + 1].hex()))
            
    def settings_load(self, fileName = 'default.json'):
        self.updating = True
        values = {}
        
        #defaults
        values['logo'] = ['logo', 'fixed', [b'\xff\xff\xff'], 'slower']
        values['ring'] = ['ring', 'super-fixed', [b'\xff\xff\xff', b'\xff\x00\x00', b'\xffU\x00', b'\xff\xff\x00', b'\x00\xff\x00', b'\x00\x80\xff', b'\x00\x00\xff', b'\xff\x00\x7f', b'\xff\x00\xff'], 'normal']

        if (os.path.isfile(fileName)):
            try:
                with open(fileName, "r") as file:
                    data = json.load(file)

                if (len(data) != 2):
                    raise KeyError("File is not formatted properly")

                for channel in data:
                    if ((channel in _channels) and (len(data[channel]) == 3)):
                        mode = data[channel]['mode']
                        colors = list(map(bytes.fromhex, data[channel]['colors']))
                        speed = data[channel]['speed']
                        values[channel] = [channel, mode, colors, speed]
                    else:
                        raise KeyError("The file is not a JSON ")
                print("Imported data!")
            except:
                raise KeyError("File is not a NZXQT Lighting JSON Profile")
        
        self.preset['logo'].values = values['logo']
        self.preset['ring'].values = values['ring']

        # always reassign colors
        self.preset['logo'].colors = self.preset['sync'].colors = self.preset['ring'].colors

        self.ui.radioButtonPresetLogo.click()
        self.preset_save()

    def preset_changed(self, attr):
        self.set_ui_value_to_preset_attr(self.sender(), attr)
 
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ring_widget_init()
        self.color_dialog_init()
        self.menu_device_reload()

        self.ui.comboBoxPresetModes.currentTextChanged.connect(self.light_preset_highlight_valid_slices)
        self.ui.pushButtonPresetSave.clicked.connect(self.preset_save)
        self.ui.pushButtonPresetImport.clicked.connect(self.preset_file_import)
        self.ui.pushButtonPresetExport.clicked.connect(self.preset_file_export)
        self.ui.labelLogo.mousePressEvent = self.logo_selected
        self.ui.radioButtonPresetLogo.clicked.connect(self.logo_selected)
        self.ui.radioButtonPresetRing.clicked.connect(self.ring_selected)
        self.ui.radioButtonPresetBoth.clicked.connect(self.both_selected)
        self.ui.horizontalSliderASpeed.valueChanged.connect(self.update_animation_speed_label)

        self.ui.actionSave.triggered.connect(self.menu_file_save)
        self.ui.actionReload.triggered.connect(self.menu_device_reload)
        #self.ui.actionNew.triggered.connect(self.menu_action_new)
        self.ui.actionExit.triggered.connect(quit)
        self.ui.labelPresetRevert.mouseReleaseEvent = self.revert_color_state

        self.preset = {}

        for channel in _channels:
            self.preset[channel] = DeviceLightingPreset(self.device, channel)
            self.preset[channel].changed.connect(self.preset_changed)

        self.settings_load()
        self.check_revert_state()

app = QtWidgets.QApplication(sys.argv)

my_mainWindow = MainWindow()
my_mainWindow.show()

sys.exit(app.exec_())
