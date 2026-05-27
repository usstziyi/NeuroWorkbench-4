__all__ = [
    "BandPowerWidget",
    "ControlPanel",
    "EEGWidget",
    "PSDWidget",
    "MainWindow",
    "ReadWidget",
    "TimeFreqWidget",
]

from widget.main_window import MainWindow
from widget.control_panel import ControlPanel
from widget.eeg_widget import EEGWidget
from widget.read_widget import ReadWidget
from widget.psd_widget import PSDWidget
from widget.band_power_widget import BandPowerWidget
from widget.time_freq_widget import TimeFreqWidget
