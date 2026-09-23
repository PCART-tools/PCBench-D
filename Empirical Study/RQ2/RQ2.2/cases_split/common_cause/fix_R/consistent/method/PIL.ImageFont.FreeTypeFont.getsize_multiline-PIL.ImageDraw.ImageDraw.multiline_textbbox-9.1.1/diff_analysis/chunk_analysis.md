# Diff 分块分析：src.PIL.ImageFont.FreeTypeFont.getsize_multiline-src.PIL.ImageDraw.ImageDraw.multiline_textbbox-9.1.1
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/src.PIL.ImageFont.FreeTypeFont.getsize_multiline-src.PIL.ImageDraw.ImageDraw.multiline_textbbox-9.1.1/src.PIL.ImageFont.FreeTypeFont.getsize_multiline/Vi-1_9.1.1.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/src.PIL.ImageFont.FreeTypeFont.getsize_multiline-src.PIL.ImageDraw.ImageDraw.multiline_textbbox-9.1.1/src.PIL.ImageFont.FreeTypeFont.getsize_multiline/Vi_9.2.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/src.PIL.ImageFont.FreeTypeFont.getsize_multiline-src.PIL.ImageDraw.ImageDraw.multiline_textbbox-9.1.1/R_candidates/10.0.0/src.PIL.ImageDraw.ImageDraw.multiline_textbbox.py
- 实验组：fix_R
- 总变更：+13 / -6 行
- 分块数：3

## Block 1 — block_001.patch
定位：@@ -10,2 +10,6 @@
说明：.. deprecated:: 9.2.0、、Use :py:meth:`.ImageDraw.multiline_textbbox` instead....

## Block 2 — block_002.patch
定位：@@ -49,2 +53,3 @@
说明：deprecate("getsize_multiline", 10, "ImageDraw.multiline_text

## Block 3 — block_003.patch
定位：@@ -51,8 +56,10 @@
说明：line_spacing = self.getsize("A", stroke_width=stroke_width)[、for line in lines:、line_width, line_height = self.getsize(...
