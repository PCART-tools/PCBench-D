# Diff 分块分析：lib.matplotlib.colorbar.Colorbar.on_mappable_changed-lib.matplotlib.colorbar.Colorbar.update_normal-v3.0.3
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/lib.matplotlib.colorbar.Colorbar.on_mappable_changed-lib.matplotlib.colorbar.Colorbar.update_normal-v3.0.3/lib.matplotlib.colorbar.Colorbar.on_mappable_changed/Vi-1_v3.0.3.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/lib.matplotlib.colorbar.Colorbar.on_mappable_changed-lib.matplotlib.colorbar.Colorbar.update_normal-v3.0.3/lib.matplotlib.colorbar.Colorbar.on_mappable_changed/Vi_v3.1.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/lib.matplotlib.colorbar.Colorbar.on_mappable_changed-lib.matplotlib.colorbar.Colorbar.update_normal-v3.0.3/R_candidates/v3.5.0/lib.matplotlib.colorbar.Colorbar.update_normal.py
- 实验组：fix_R
- 总变更：+1 / -2 行
- 分块数：1

## Block 1 — block_001.patch
定位：@@ -8,4 +8,3 @@
说明：self.set_cmap(mappable.get_cmap())、self.set_clim(mappable.get_clim())、_log.debug('colorbar mappable changed')
