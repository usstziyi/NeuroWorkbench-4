from dataclasses import dataclass

import numpy as np

BAND_DEFS = {
    "delta": (0.5, 4.0),
    "theta": (4.0, 8.0),
    "alpha": (8.0, 13.0),
    "beta": (13.0, 30.0),
    "gamma": (30.0, 45.0),
}

@dataclass
class BandPowerResult:
    band_powers: list


class BandPowerAnalyzer:
    def compute(self, psd: np.ndarray, freqs: np.ndarray,) -> BandPowerResult:
        # 对每个通道的 PSD 在全频段上做 梯形积分 ，得到每个通道的总功率。结果是形状为 (通道数,) 的一维数组。
        total_power = np.trapezoid(psd, freqs, axis=1)
        band_powers: list = []
        # 逐个处理每个通道的 PSD 曲线及其对应的总功率
        for ch_psd, total in zip(psd, total_power):
            ch_powers: dict[str, float] = {}
            # 遍历五个标准频段
            for band_name, (low, high) in BAND_DEFS.items():
                mask = (freqs >= low) & (freqs <= high)
                if not np.any(mask):
                    ch_powers[band_name] = 0.0
                    continue
                # 用布尔掩码筛选出属于该频段的频率点，然后在此范围内做梯形积分得到 绝对功率
                abs_power = float(np.trapezoid(ch_psd[mask], freqs[mask]))
                ch_powers[band_name] = float(abs_power / total) if total > 0 else 0.0
            band_powers.append(ch_powers)
        return BandPowerResult(band_powers=band_powers)


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