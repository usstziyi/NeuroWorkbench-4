import pyqtgraph as pg
from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6 import QtGui, QtCore
import numpy as np



class TimeFreqWidget(pg.GraphicsLayoutWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self._sample_rate: int = 250


        """
        plot = win.addPlot()
        image = pg.ImageItem()
        plot.addItem(image)
        image.setImage(img_data)
        """
        self._plot = self.addPlot()
        self._plot.setLabel("bottom", "frequency", units="Hz")
        self._plot.setLabel("left", "history", units="frame")
        self._plot.getAxis("left").setWidth(60)
        self._plot.getAxis("bottom").autoSIPrefix = False
        self._plot.getAxis("left").autoSIPrefix = False
        self.spec_bottom_axis = self._plot.getAxis("bottom")
        # self._plot.invertY(True) # 翻转Y轴
        self.spec_image = pg.ImageItem(data=None, axisOrder="row-major")
        cmap = pg.colormap.get("plasma") #plasma #magma
        self.spec_image.setLookupTable(cmap.getLookupTable(nPts=256))
        self._plot.addItem(self.spec_image)
        # 添加标记线
        self._plot.addLine(x=50, pen=pg.mkPen('w', width=2, style=pg.QtCore.Qt.PenStyle.DotLine),
                                    movable=True, label='{value:0.2f}Hz',labelOpts={'position': 0.5})
        self._plot.setXRange(0, 60)
        self._plot.setYRange(0, 120)

    

    def update_data(self, spectrogram: np.ndarray, sample_rate: int = 250) -> None:
        n_frames, n_bins = spectrogram.shape
        nyquist = sample_rate / 2
        # 默认情况下，如果你没有额外设置 setRect() 或 transform，那么这张图像会按数组索引坐标显示
        self.spec_image.setImage(spectrogram, autoLevels=True)
        if n_bins > 1 and nyquist > 0:
            # 每个频率箱的频率宽度：频率分辨率
            self.spec_image.setRect(
                # 把图像映射到：
                # x: [0 , nyquist]
                # y: [0 , n_frames]
                QtCore.QRectF(0, 0, 60, n_frames)
                # QtCore.QRectF(-bin_width / 2, 0, nyquist + bin_width, n_frames)
            )