import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6 import QtGui


CET_R3 = [
    (214, 68, 60),
    (239, 143, 44),
    (200, 202, 52),
    (65, 183, 130),
    (50, 138, 190),
    (80, 82, 185),
    (139, 61, 159),
    (197, 50, 120),
]


class PSDWidget(QWidget):
    def __init__(self, channels: int = 1, parent: QWidget | None = None):
        super().__init__(parent)
        self._plot_widget = pg.PlotWidget()
        self._plot_widget.setLabel("left", "Power Spectral Density", units="µV²/Hz")
        self._plot_widget.setLabel("bottom", "Frequency", units="Hz")
        self._plot_widget.getAxis("left").autoSIPrefix = False
        self._plot_widget.getAxis("bottom").autoSIPrefix = False
        self._plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self._plot_widget.setLogMode(x=False, y=True)
        self._plot_widget.setYRange(-3, 9)

        self._plot_widget.setDownsampling(auto=True, mode="peak")
        self._plot_widget.setClipToView(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._plot_widget)

        font = QtGui.QFont()
        font.setPointSize(6)
        self._plot_widget.getAxis("left").setStyle(tickFont=font)

        self._num_channels = channels
        self._curve = {}

        for i in range(channels):
            color = CET_R3[i % len(CET_R3)]
            self._curve[i] = self._plot_widget.plot(pen=pg.mkPen(color, width=1.5))


    def set_freq_range(self, max_freq: float) -> None:
        self._plot_widget.setXRange(0, max_freq)

    def update_psd(self, freqs: np.ndarray, psd_values: np.ndarray) -> None:
        if freqs.size == 0 or psd_values.size == 0:
            return
        # 将PSD值限制在最小值1e-12以上，避免对数坐标下出现零或负值
        psd_values = np.maximum(psd_values, 1e-12)


        # 如果psd_values是一维的,转成二维
        if psd_values.ndim == 1:
            psd_values = psd_values[np.newaxis, :]


        for i in range(self._num_channels):
            self._curve[i].setData(freqs, psd_values[i])
