# Diff 分块分析：lib.matplotlib.backend_bases.GraphicsContextBase.set_linestyle-lib.matplotlib.backend_bases.GraphicsContextBase.set_dashes-v1.5.3
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/lib.matplotlib.backend_bases.GraphicsContextBase.set_linestyle-lib.matplotlib.backend_bases.GraphicsContextBase.set_dashes-v1.5.3/lib.matplotlib.backend_bases.GraphicsContextBase.set_linestyle/Vi-1_v1.5.3.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/lib.matplotlib.backend_bases.GraphicsContextBase.set_linestyle-lib.matplotlib.backend_bases.GraphicsContextBase.set_dashes-v1.5.3/lib.matplotlib.backend_bases.GraphicsContextBase.set_linestyle/Vi_v2.0.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/lib.matplotlib.backend_bases.GraphicsContextBase.set_linestyle-lib.matplotlib.backend_bases.GraphicsContextBase.set_dashes-v1.5.3/R_candidates/v3.0.0/lib.matplotlib.backend_bases.GraphicsContextBase.set_dashes.py
- 实验组：fix_R
- 总变更：+4 / -16 行
- 分块数：3

## Block 1 — block_001.patch
定位：@@ -3,9 +3,6 @@
说明：'dotted'). One may specify customized dash styles by providi、a tuple of (offset, dash pairs). For example, the predefiend、linestyles have following values.:...

## Block 2 — block_002.patch
定位：@@ -11,10 +8,2 @@
说明：、if style in self.dashd:、offset, dashes = self.dashd[style]...

## Block 3 — block_003.patch
定位：@@ -20,2 +9,1 @@
说明：self.set_dashes(offset, dashes)
