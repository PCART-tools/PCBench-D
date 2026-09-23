# Diff 分块分析：scipy.optimize.anneal.anneal-scipy.optimize._basinhopping.basinhopping-v0.10.1
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/function/scipy.optimize.anneal.anneal-scipy.optimize._basinhopping.basinhopping-v0.10.1/scipy.optimize.anneal.anneal/Vi-1_v0.10.1.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/function/scipy.optimize.anneal.anneal-scipy.optimize._basinhopping.basinhopping-v0.10.1/scipy.optimize.anneal.anneal/Vi_v0.11.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/function/scipy.optimize.anneal.anneal-scipy.optimize._basinhopping.basinhopping-v0.10.1/R_candidates/v0.16.0/scipy.optimize._basinhopping.basinhopping.py
- 实验组：fix_R
- 总变更：+29 / -77 行
- 分块数：9

## Block 1 — block_001.patch
定位：@@ -11,3 +11,3 @@
说明：lower=-100, upper=100, dwell=50):、lower=-100, upper=100, dwell=50, disp=True):

## Block 2 — block_002.patch
定位：@@ -19,3 +19,3 @@
说明：func : callable f(x, *args)、func : callable ``f(x, *args)``

## Block 3 — block_003.patch
定位：@@ -54,2 +54,4 @@
说明：disp : bool、Set to True to print convergence messages.

## Block 4 — block_004.patch
定位：@@ -78,2 +80,7 @@
说明：、See also、--------...

## Block 5 — block_005.patch
定位：@@ -135,5 +142,2 @@
说明：x0 = asarray(x0)、lower = asarray(lower)、upper = asarray(upper)

## Block 6 — block_006.patch
定位：@@ -139,7 +143,18 @@
说明：schedule = eval(schedule+'_sa()')、#   initialize the schedule、schedule.init(dims=shape(x0),func=func,args=args,boltzmann=b...

## Block 7 — block_007.patch
定位：@@ -145,66 +160,3 @@
说明：current_state, last_state, best_state = _state(), _state(), 、if T0 is None:、x0 = schedule.getstart_temp(best_state)...

## Block 8 — block_008.patch
定位：@@ -211,4 +163,4 @@
说明：return best_state.x, best_state.cost, schedule.T, \、schedule.feval, iters, schedule.accepted, retval、return res['x'], res['fun'], res['T'], res['nfev'], res['nit...

## Block 9 — block_009.patch
定位：@@ -214,2 +166,2 @@
说明：return best_state.x, retval、return res['x'], res['status']
