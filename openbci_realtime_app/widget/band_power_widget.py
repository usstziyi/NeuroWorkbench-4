import pyqtgraph as pg
from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6 import QtGui


class BandPowerWidget(pg.GraphicsLayoutWidget):
    BAND_DEFS = {
        "delta": (0.5, 4.0),
        "theta": (4.0, 8.0),
        "alpha": (8.0, 13.0),
        "beta": (13.0, 30.0),
        "gamma": (30.0, 45.0),
    }

    CHANNEL_COLORS = [
        (100, 180, 255),
        (255, 150, 100),
        (100, 255, 150),
        (255, 200, 80),
        (180, 120, 255),
        (255, 120, 180),
        (120, 255, 220),
        (220, 220, 100),
    ]

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

    def __init__(self, channels: int = 8, parent: QWidget | None = None):
        super().__init__(parent)

        self._num_channels = channels
        self._bar_items: list[pg.BarGraphItem] = []

        font = QtGui.QFont()
        font.setPointSize(6)

        self._plot_widget = self.addPlot()
        self._plot_widget.setLabel("left", "Relative Power")
        self._plot_widget.getAxis("left").setWidth(60)
        self._plot_widget.getAxis("left").setStyle(tickFont=font)
        self._plot_widget.setLabel("bottom", "Frequency Band")
        self._plot_widget.showGrid(y=True, alpha=0.3)
        band_names = list(self.BAND_DEFS.keys())
        self._plot_widget.setXRange(0, len(band_names) - 1, padding=0.15)
        self._plot_widget.setYRange(0, 1.0)

        x_axis = self._plot_widget.getAxis("bottom")
        x_axis.setTicks([[
            (i, f"{name}\n({lo:.3g}-{hi:.3g} Hz)")
            for i, (name, (lo, hi)) in enumerate(self.BAND_DEFS.items())
        ]])
        bar_width = 0.8 / max(self._num_channels, 1)
        for i in range(self._num_channels):
            color = self.CET_R3[i % len(self.CET_R3)]
            bar = pg.BarGraphItem(
                x=[], 
                height=[], 
                width=bar_width, 
                brush=color
            )
            self._plot_widget.addItem(bar)
            self._bar_items.append(bar)

    def update_band_powers(self, band_powers: list[dict]) -> None:
        if not band_powers or not self._bar_items:
            return
        num_ch = len(self._bar_items)
        # 每个通道的条形图宽度
        bar_width = 0.8 / max(num_ch, 1)
        for ch_idx, bp in enumerate(band_powers[:num_ch]):
            heights = [bp.get(name, 0.0) for name in self.BAND_DEFS]
            offset = (ch_idx - (num_ch - 1) / 2.0) * bar_width
            x = [i + offset for i in range(len(self.BAND_DEFS))]
            self._bar_items[ch_idx].setOpts(
                x=x,
                height=heights, 
                width=bar_width
            )


"""
band_powers
[
    {"delta": 0.12, "theta": 0.08, "alpha": 0.45, "beta": 0.25, "gamma": 0.10},  # 通道1
    {"delta": 0.15, "theta": 0.10, "alpha": 0.40, "beta": 0.20, "gamma": 0.15},  # 通道2
    {"delta": 0.18, "theta": 0.07, "alpha": 0.35, "beta": 0.30, "gamma": 0.10},  # 通道3
    {"delta": 0.10, "theta": 0.12, "alpha": 0.50, "beta": 0.18, "gamma": 0.10},  # 通道4
    {"delta": 0.14, "theta": 0.09, "alpha": 0.42, "beta": 0.22, "gamma": 0.13},  # 通道5
    {"delta": 0.11, "theta": 0.11, "alpha": 0.38, "beta": 0.28, "gamma": 0.12},  # 通道6
    {"delta": 0.16, "theta": 0.08, "alpha": 0.44, "beta": 0.21, "gamma": 0.11},  # 通道7
    {"delta": 0.13, "theta": 0.10, "alpha": 0.41, "beta": 0.24, "gamma": 0.12},  # 通道8
]
"""