import math

geometry = [
    "s",
    "s",
    "s",
    "s",
    "s",
    "s",
    "s",
    "s",
    "r",
    "r",
    "r",
    "s",
]
size = [
    [0.01, 0.01],
    [0.01, 0.01],
    [0.01, 0.01],
    [0.01, 0.01],
    [0.01, 0.01],
    [0.01, 0.01],
    [0.01, 0.01],
    [0.01, 0.01],
    [0.02, 0.01],
    [0.02, 0.01],
    [0.02, 0.01],
    [0.02, 0.02],
]
angle = [0, 0, 0, 0, 0, 0, 0, 0, 0, math.pi / 2, math.pi / 2, 0]
intensity = [
    [1000, 2000],
    [1000],
    [1000],
    [1000],
    [1000],
    [1000],
    [1000],
    [1000],
    [1000],
    [1000],
    [1000],
    [1000],
]

# for powers sampling test
intensity_p = [
    ["uniform", 2000, 3000],  # 2000-3000 均匀采样 (不包括3000)
    ["uniform", 1000, 2000, 100],  # 1000-2000间隔100采样，包括2000
    [1000, 2000],  # 两者随机选一
    [1000],  # 固定
    [1000],
    [1000],
    [1000],
    [1000],
    [1000],
    [1000],
    [1000],
    [1000],
]
position = [
    [0.01927952, 0.09154201],
    [0.09288323, 0.07906539],
    [0.04514527, 0.01451643],
    [0.00656708, 0.01069035],
    [0.07232013, 0.08852603],
    [0.02580174, 0.033368],
    [0.02121442, 0.06563024],
    [0.04655992, 0.0694678],
    [0.08187908, 0.06275452],
    [0.02189589, 0.01398727],
    [0.04872661, 0.05303207],
    [0.07691146, 0.03140043],
]
