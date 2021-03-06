# -*- coding: utf-8 -*-
import sys, os
import mainwindow as mainwindow
import usb.core

from PyQt5 import Qt, QtGui, QtCore, QtWidgets, QtChart
from PyQt5.QtGui import QPalette

import itertools
import json

from liquidctl.driver.kraken_two import KrakenTwoDriver
from liquidctl.driver.nzxt_smart_device import NzxtSmartDeviceDriver

from liquidctl.common.preset import DeviceLightingPreset
from liquidctl.common.qringwidget import QRingWidget

from liquidctl.common.graphs  import *
import pyqtgraph as pg

DRIVERS = [
    KrakenTwoDriver,
    NzxtSmartDeviceDriver,
]

_channels = ['logo', 'ring', 'sync']
_attributes = ['channel', 'mode', 'colors', 'speed']

DEFAULT_CONFIG = {
    "device" : None,
    "preset" : {
        "logo": {
            "channel": "logo",
            "colors": ["#ffffff"],
            "mode": "fixed",
            "speed": "slower"
        },
        "ring": {
            "channel": "ring",
            "colors": ["#ffffff", "#ff0000", "#ff7f00", "#ffff00", "#00ff00", "#007fff", "#0000ff", "#7f00ff", "#ff007f"],
            "mode": "spectrum-wave",
            "speed": "normal"
        }
    },
    "fan_ctl" : [[0, 0], [30, 30], [50, 70], [60, 100]], 
    "pump_ctl" : [[0, 0], [30, 30], [50, 70], [80, 100]]
}

def find_all_supported_devices():
    res = map(lambda driver: driver.find_supported_devices(), DRIVERS)
    return itertools.chain(*res)

class MainWindow(QtWidgets.QMainWindow):

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
        """Highlights ring segments or logo valid for the preset"""
        mode = self.get_ui_value_of_preset_attr('mode')
        if mode == '':
            mode = self.ui.labelRingMode.text().lower()
            if mode == '':
                return

        mval, mod2, mod4, mincolors, maxcolors, ringonly = self.device.get_color_modes()[mode]
        
        self.widget.highlight_slices(maxcolors, self.picked)
        
        font = self.ui.labelLogo.font()
        font.setUnderline(self.picked == self.ui.labelLogo)
        self.ui.labelLogo.setFont(font)
    
    def update_animation_speed_label(self, value: str):
        """Updates animation speed information"""
        speed = self.get_ui_value_of_preset_attr('speed')
        self.ui.labelPresetAniSpeedLabel.setText("Animation Speed: %s" % speed.title())

    def light_device_selected(self):
        """Updates the interface when a device has been selected"""

        if ((not self.device is None) and (hasattr(self.device, 'device'))):
            self.device.connect()
        else:
            raise UnboundLocalError("The selected device is not available")

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
            self.update_ui_from_preset()
    
    def show_preset_file_import_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Import Lighting Preset", "","NZXQT Lighting JSON Profile(*.json)", options=options)
        if fileName:
            self.import_presets_from_file(fileName)
    def show_preset_file_export_dialog(self):
        #
        # FIXME when the export button is pressed, we require the settings to be saved to the device (and self.preset), 
        #       otherwise the data will export only values in self.preset, not the values currently shown in the UI
        #
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None,"Export Lighting Preset","","NZXQT Lighting JSON Profile(*.json)", options=options)

        if fileName:
            self.export_presets_to_file(fileName)
    
    def import_presets_from_file(self, fileName):
        self.updating = True

        # use the defaults from read_config()
        values  = self.config['preset']
        data = values
        
        if (os.path.isfile(fileName)):
            with open(fileName, "r") as file:
                data = json.load(file)

            if (not isinstance(data, dict)):
                raise KeyError("File is not formatted properly")

            if ('preset' in data):
                # allow importing config files
                data = data['preset']

            for channel in data:
                if (channel in _channels) :
                    mode = data[channel]['mode']
                    colors = data[channel]['colors']
                    speed = data[channel]['speed']
                    values[channel] = [channel, mode, colors, speed]
                else:
                    raise KeyError("The file is not a JSON ")
            print("Imported data!")
        
        self.preset['logo'].values = values['logo']
        self.preset['ring'].values = values['ring']

        # always reassign colors
        self.preset['logo'].colors = self.preset['sync'].colors = self.preset['ring'].colors

        self.ui.radioButtonPresetLogo.click()
        self.write_presets_to_device()
    def export_presets_to_file(self, fileName):

        presets = {}

        for channel in ['logo', 'ring']:
            data = {}
            for attr in ['mode', 'colors', 'speed']:
                value = getattr(self.preset[channel], attr)
                if (attr == 'colors'):
                    if (channel == 'logo'):
                        value = []
                data[attr] = value
            presets[channel] = data

        try:
            with open(fileName, "w") as file:
                json.dump(presets, file, sort_keys=False, indent=4)
        except:
            raise SystemError("Could not write to the file '%s" % fileName)
   
    def write_presets_to_device(self):
        """saves values to preset based on currenly selected channel"""
        if (self.device == None):
            return

        current_channel = self.get_ui_value_of_preset_attr('channel')

        self.updating = (current_channel == 'sync') # allow all labels to update when sync, otherwise they update later
        self.preset[current_channel].values = list(map(self.get_ui_value_of_preset_attr, _attributes))

        if (current_channel == 'sync'):
            self.preset['ring'].values = self.preset[current_channel].values
            self.preset['logo'].values = self.preset[current_channel].values

        self.preset['logo'].write()
        self.preset['ring'].write()

        self.updating = True
        self.update_ui_from_preset()
        self.save_config()

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
        self.last_color = self.widget.last_slice.color()
        self.set_picked_slice(self.widget.last_slice)
        self.update_ui_from_preset(self.preset['ring'])
    
    def ring_widget_init(self):
        """Adds a ring widget as a QChart"""
        self.widget = QRingWidget(self.ui.frameLightingWidget)
        self.widget.setBackgroundColor(self.ui.tab_2_1.palette().color(4))
        
        self.widget.slice_clicked.connect(self.ring_widget_slice_clicked)
        self.widget.slice_hovered.connect(self.ring_widget_slice_hovered)
        self.widget.slice_dblclicked.connect(self.ring_widget_slice_dblclicked)

        self.picked = self.widget.last_slice
    def ring_widget_slice_clicked(self, pieslice):
        """Stores slice and sets color dialog color"""
        self.set_picked_slice(pieslice)
    def ring_widget_slice_dblclicked(self):
        """Fills all slices with the same color"""
        self.widget.fill_slices(self.last_color)
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
        self.colorDialog.done = lambda x: None #captures the event that would otherwise cause the colordialog to disappear
        window = self.ui.mdiArea.addSubWindow(self.colorDialog, flags=QtCore.Qt.FramelessWindowHint)
        window.showMaximized()

    def check_revert_state(self):
        """ compares user-interface values to those in the preset, toggles enabled state of revert label"""
        channel = self.get_ui_value_of_preset_attr('channel')
        revert = (self.get_ui_value_of_preset_attr('colors') != getattr(self.preset[channel], 'colors'))

        self.ui.labelPresetRevert.setEnabled(revert)
    def revert_color_state(self, evt):
        """ restores the color chart values on the user-interface from those in the current channels preset """
        for channel in _channels:
            self.set_ui_value_to_preset_attr(self.preset[channel], 'colors')

        self.update_ui_from_preset()

        if (isinstance(self.picked, QtChart.QPieSlice)):
            color = self.picked.color()
        else:
            color = self.get_logo_qcolor()

        self.colorDialog.setCurrentColor(color)

    def update_ui_from_preset(self, preset: DeviceLightingPreset = None):
        """ updates ui values for the given preset data """
        current_channel = self.get_ui_value_of_preset_attr('channel')
        if (preset == None):
            preset = self.preset[current_channel]

        for attr in _attributes:
            if ((current_channel == preset.channel) and (attr == 'colors')):
                continue
            self.set_ui_value_to_preset_attr(preset, attr)

        self.check_revert_state()

    def get_ui_value_of_preset_attr(self, attr):
        """ 
        returns the corresponding user-interface attribute value(s) for one the following:

        Parameters::
        `channel` - the channel id given to the checked radio button\n
        `mode` - the preset combobox currently selected mode text\n
        `colors` - an array of both the logo and ring widget colors\n 
        `speed` - a string matching the current speed setting
        """
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
            channel = self.get_ui_value_of_preset_attr('channel')

            colors = [self.get_logo_qcolor().name()]
            if (channel == 'logo'):
                return colors

            for i, ps in enumerate(self.widget.slices()):
                color = self.widget.slices()[i].color().name()
                colors.append(color)

            return colors

        if (attr == 'speed'):
            speed = self.ui.horizontalSliderASpeed.value()
            for name, value in self.device.get_animation_speeds().items():
                if (value == speed):
                    return name
    def set_ui_value_to_preset_attr(self, preset: DeviceLightingPreset, attr: str):
        """ 
        allows user interfaces attribute to be set from a preset attribute 
        
        Parameters::
        `preset` - a DeviceLightingPreset to acquire attribute data from\n
        `attr` - the name of the attribute data to acquire, must be either 'channel', 'mode', 'colors', or 'speed'
        """
        if (not isinstance(preset, DeviceLightingPreset)):
            raise TypeError("The object is not of type DeviceLightingPreset")
        
        # sometimes we are called by someone who doesn't want us
        if (not self.updating):
            return

        # grab the common objects
        if (preset.channel == 'logo'):
            label = self.ui.labelLogoMode
            radio = self.ui.radioButtonPresetLogo
        elif (preset.channel == 'ring'):
            label = self.ui.labelRingMode
            radio = self.ui.radioButtonPresetRing
        else:
            label = self.ui.labelBothMode
            radio = self.ui.radioButtonPresetBoth

        # just setting the radio button 
        if (attr == 'channel'):
            radio.setChecked(True)

        elif (attr == 'mode'):
            mode = preset.mode.title()
            self.ui.comboBoxPresetModes.setCurrentText(mode)

            label.setText(mode)

            if (self.preset['ring'].mode == self.preset['logo'].mode):
                self.preset['sync'].mode = mode
                self.ui.labelBothMode.setText(mode)
            else:
                self.ui.labelBothMode.setText("Mixed-Mode")

        elif (attr == 'speed'):
            if (preset.speed not in preset.speeds):
                return
            self.ui.horizontalSliderASpeed.setValue(preset.speeds[preset.speed])
            
        elif (attr == 'colors'):
            if (preset.channel == 'logo'):
                color = QtGui.QColor(preset.colors[0])
                palette = self.ui.labelLogo.palette()
                palette.setColor(0, color)
                self.ui.labelLogo.setPalette(palette)
            if (preset.channel == 'ring'):
                for i, ps in enumerate(self.widget.slices()):
                    if (i >= (len(preset.colors) - 1)):
                        break
                    ps.setColor(QtGui.QColor(preset.colors[i + 1]))
        else:
            raise AttributeError("Could not set unknown attribute '%s'" % attr)

    def preset_changed(self, attr):
        self.set_ui_value_to_preset_attr(self.sender(), attr)

    def graph_init(self, graphView, xlabel, ylabel):
        InitPlotWidget(
            graphView, 
            labels={'left': xlabel, 'bottom': ylabel},
            showGrid={'x': True, 'y': True, 'alpha': 0.1},
            tickSpacing={'left': (10, 1), 'bottom': (10, 1)},
            limits=(-3, 110)
        )

        color = graphView.palette().color(QPalette.Dark).name()
        graphView.setBackground(color)
        graphView.setStyleSheet("background-color: %s; border-style: solid; border-color: %s; border-width: 2px; border-radius: 5px;" % ( color, color ) )
    
    def xctl_graph_init(self, parent: PlotWidget, xName, data: list):
        self.graph_init(parent, [f'{xName} Duty', '%'], ["Temperature", '°C'])

        pen = pg.mkPen('w', width=0.2, style=QtCore.Qt.DashLine)
        xline = pg.InfiniteLine(pos=0, pen=pen, name="currTemp", angle=270)
        yline = pg.InfiniteLine(pos=0, pen=pen, name=f"curr{xName}", angle=0)

        pg.InfLineLabel(xline, text="{value}°C", position=0.04, rotateAxis=(0,0))
        pg.InfLineLabel(yline, text="{value}%", position=0, rotateAxis=(0,0))

        graph = EditableGraph(parent, data=data )

        parent.addItem(graph)
        parent.addItem(xline)
        parent.addItem(yline)


    def ctl_timer_init(self):
        self.ctl_timer = QtCore.QTimer()
        self.ctl_timer.timeout.connect(self.ctl_timer_tick)
        self.ctl_timer.start(500)

    def ctl_timer_tick(self):
        if self.device is None:
            return
        
        device_rpmlimit_fan = 1400
        device_rpmlimit_pump = 2700

        status = self.device.get_status()

        temp = int(status[0][1])
        fan = int( ( status[1][1] / device_rpmlimit_fan ) * 100 )
        pump = int( ( status[2][1] / device_rpmlimit_pump ) * 100 )

        get_plotwidget_item(self.ui.graphicsViewFanCtl, 'currTemp').setValue(temp)
        get_plotwidget_item(self.ui.graphicsViewFanCtl, 'currFan').setValue(fan)

        get_plotwidget_item(self.ui.graphicsViewPumpCtl, 'currTemp').setValue(temp)
        get_plotwidget_item(self.ui.graphicsViewPumpCtl, 'currPump').setValue(pump)

        self.config['fan_ctl'] = graph_from_widget(self.ui.graphicsViewFanCtl).pos.tolist()
        self.config['pump_ctl'] = graph_from_widget(self.ui.graphicsViewPumpCtl).pos.tolist()

    def load_config(self):
        """ reads the default configuration file into self.config tuple """
        temp_config = DEFAULT_CONFIG

        try:
            with open("config.json", "r") as file:
                temp_config = json.load(file)
        except:
            print("Could not open file, using the default config...")

        # use default values for those that we could not load
        temp_config = dict(DEFAULT_CONFIG, **temp_config)

        for key in ['fan_ctl', 'pump_ctl']:
            if ( len(temp_config[key]) < 2):
                temp_config[key] = DEFAULT_CONFIG[key]
            temp_config[key] = sorted(temp_config[key], key=lambda tup: tup[1])
        
        self.config = temp_config
        #self.save_config()

    def save_config(self):
        try:
            if (hasattr(self, 'preset')):
                self.config['preset']['logo'] = self.preset['logo'].to_json()
                self.config['preset']['ring'] = self.preset['ring'].to_json()

            with open("config.json", "w") as file:
                json.dump(self.config, file, sort_keys=False, indent=4)

                print("Saved config, data: %s " % self.config)
        except Exception as e:
            print("Failed to save config! %s" % e)

    def graph_append_point(self):
        if (self.sender() == self.ui.pushButtonFanCtlAppend):
            graphicsView = self.ui.graphicsViewFanCtl
        else:
            graphicsView = self.ui.graphicsViewPumpCtl
        
        graph_from_widget(graphicsView).addPoint()

    def graph_delete_point(self):
        if (self.sender() == self.ui.pushButtonFanCtlDelete):
            graphicsView = self.ui.graphicsViewFanCtl
        else:
            graphicsView = self.ui.graphicsViewPumpCtl

        graph_from_widget(graphicsView).removePoint()

    def menu_reset(self):
        raise NotImplementedError()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.load_config()
        self.xctl_graph_init(self.ui.graphicsViewFanCtl, 'Fan', self.config['fan_ctl'])
        self.xctl_graph_init(self.ui.graphicsViewPumpCtl, 'Pump', self.config['pump_ctl'])
        self.ctl_timer_init()

        self.ring_widget_init()
        self.color_dialog_init()
        self.menu_device_reload()

        self.ui.comboBoxPresetModes.currentTextChanged.connect(self.light_preset_highlight_valid_slices)
        self.ui.pushButtonPresetSave.clicked.connect(self.write_presets_to_device)
        self.ui.pushButtonPresetImport.clicked.connect(self.show_preset_file_import_dialog)
        self.ui.pushButtonPresetExport.clicked.connect(self.show_preset_file_export_dialog)
        self.ui.labelLogo.mousePressEvent = self.logo_selected
        self.ui.radioButtonPresetLogo.clicked.connect(self.logo_selected)
        self.ui.radioButtonPresetRing.clicked.connect(self.ring_selected)
        self.ui.radioButtonPresetBoth.clicked.connect(self.both_selected)
        self.ui.horizontalSliderASpeed.valueChanged.connect(self.update_animation_speed_label)

        self.ui.actionSave.triggered.connect(self.save_config)
        self.ui.actionReload.triggered.connect(self.menu_device_reload)
        self.ui.actionReset.triggered.connect(self.menu_reset)
        #self.ui.actionNew.triggered.connect(self.menu_action_new)
        self.ui.actionExit.triggered.connect(quit)
        self.ui.labelPresetRevert.mouseReleaseEvent = self.revert_color_state

        self.ui.pushButtonFanCtlAppend.clicked.connect(self.graph_append_point)
        self.ui.pushButtonFanCtlDelete.clicked.connect(self.graph_delete_point)

        self.ui.pushButtonPumpCtlAppend.clicked.connect(self.graph_append_point)
        self.ui.pushButtonPumpCtlDelete.clicked.connect(self.graph_delete_point)

        self.preset = {}

        for channel in _channels:
            self.preset[channel] = DeviceLightingPreset(self.device, channel)
            self.preset[channel].changed.connect(self.preset_changed)
        
        #reads presets from file
        self.import_presets_from_file("config.json")

app = QtWidgets.QApplication(sys.argv)

my_mainWindow = MainWindow()
my_mainWindow.show()

sys.exit(app.exec_())
