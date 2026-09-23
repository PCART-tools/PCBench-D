# Diff 分块分析：aiohttp.web.Application.register_on_finish-aiohttp.web.Application.on_cleanup-v0.20.2
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/aiohttp.web.Application.register_on_finish-aiohttp.web.Application.on_cleanup-v0.20.2/aiohttp.web.Application.register_on_finish/Vi-1_v0.20.2.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/aiohttp.web.Application.register_on_finish-aiohttp.web.Application.on_cleanup-v0.20.2/aiohttp.web.Application.register_on_finish/Vi_v0.21.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/aiohttp.web.Application.register_on_finish-aiohttp.web.Application.on_cleanup-v0.20.2/R_candidates/2.0.0/aiohttp.web.Application.on_cleanup.py
- 实验组：fix_R
- 总变更：+2 / -1 行
- 分块数：1

## Block 1 — block_001.patch
定位：@@ -1,2 +1,3 @@
说明：self._finish_callbacks.insert(0, (func, args, kwargs))、warnings.warn("Use .on_cleanup.append() instead", Deprecatio、self.on_cleanup.append(lambda app: func(app, *args, **kwargs
