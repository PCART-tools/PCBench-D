# Diff 分块分析：src.PIL.ImageFont.FreeTypeFont.getoffset-src.PIL.ImageFont.FreeTypeFont.getlength-9.1.1
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/candidates_cause/fix_R/consistent/method/src.PIL.ImageFont.FreeTypeFont.getoffset-src.PIL.ImageFont.FreeTypeFont.getlength-9.1.1/src.PIL.ImageFont.FreeTypeFont.getoffset/Vi-1_9.1.1.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/candidates_cause/fix_R/consistent/method/src.PIL.ImageFont.FreeTypeFont.getoffset-src.PIL.ImageFont.FreeTypeFont.getlength-9.1.1/src.PIL.ImageFont.FreeTypeFont.getoffset/Vi_9.2.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/candidates_cause/fix_R/consistent/method/src.PIL.ImageFont.FreeTypeFont.getoffset-src.PIL.ImageFont.FreeTypeFont.getlength-9.1.1/R_candidates/10.0.0/src.PIL.ImageFont.FreeTypeFont.getlength.py
- 实验组：fix_R
- 总变更：+5 / -0 行
- 分块数：2

## Block 1 — block_001.patch
定位：@@ -2,2 +2,6 @@
说明：.. deprecated:: 9.2.0、、Use :py:meth:`.getbbox` instead....

## Block 2 — block_002.patch
定位：@@ -10,2 +14,3 @@
说明：deprecate("getoffset", 10, "getbbox")
