# Diff 分块分析：src.PIL.ImageDraw.ImageDraw.multiline_textsize-src.PIL.ImageDraw.ImageDraw.multiline_textbbox-9.1.1
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/src.PIL.ImageDraw.ImageDraw.multiline_textsize-src.PIL.ImageDraw.ImageDraw.multiline_textbbox-9.1.1/src.PIL.ImageDraw.ImageDraw.multiline_textsize/Vi-1_9.1.1.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/src.PIL.ImageDraw.ImageDraw.multiline_textsize-src.PIL.ImageDraw.ImageDraw.multiline_textbbox-9.1.1/src.PIL.ImageDraw.ImageDraw.multiline_textsize/Vi_9.2.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/src.PIL.ImageDraw.ImageDraw.multiline_textsize-src.PIL.ImageDraw.ImageDraw.multiline_textbbox-9.1.1/R_candidates/10.0.0/src.PIL.ImageDraw.ImageDraw.multiline_textbbox.py
- 实验组：fix_R
- 总变更：+15 / -8 行
- 分块数：2

## Block 1 — block_001.patch
定位：@@ -10,2 +10,3 @@
说明：deprecate("multiline_textsize", 10, "multiline_textbbox")

## Block 2 — block_002.patch
定位：@@ -12,10 +13,16 @@
说明：line_spacing = (、self.textsize("A", font=font, stroke_width=stroke_width)[1] 、)...
