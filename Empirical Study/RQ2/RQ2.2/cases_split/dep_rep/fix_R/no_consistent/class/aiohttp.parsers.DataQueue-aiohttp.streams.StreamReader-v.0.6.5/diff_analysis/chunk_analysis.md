# Diff 分块分析：aiohttp.parsers.DataQueue-aiohttp.streams.StreamReader-v.0.6.5
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/class/aiohttp.parsers.DataQueue-aiohttp.streams.StreamReader-v.0.6.5/aiohttp.parsers.DataQueue/Vi-1_v.0.6.5.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/class/aiohttp.parsers.DataQueue-aiohttp.streams.StreamReader-v.0.6.5/aiohttp.parsers.DataQueue/Vi_v0.7.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/class/aiohttp.parsers.DataQueue-aiohttp.streams.StreamReader-v.0.6.5/R_candidates/v0.9.0/aiohttp.streams.StreamReader.py
- 实验组：fix_R
- 总变更：+17 / -9 行
- 分块数：3

## Block 1 — block_001.patch
定位：@@ -3,3 +3,4 @@
说明：def __init__(self, *, loop=None):、def __init__(self, stream, *, loop=None):、self._stream = stream

## Block 2 — block_002.patch
定位：@@ -9,2 +10,5 @@
说明：、def at_eof(self):、return self._eof

