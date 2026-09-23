# 一、突变情况分析

- **Total**: 215
- **替代API**: `scipy.optimize._basinhopping.basinhopping`
- **10% 阈值**: 21.5

## Vi-1 (v0.10.1-v0.16.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 5 | 0.4105 |
| tokenBased | 13 | 0.5011 |
| treeBased | 6 | 0.4335 |

## Vi (v0.11.0-v0.16.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 89 | 0.2517 |
| tokenBased | 71 | 0.2305 |
| treeBased | 25 | 0.3959 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 5 | 89 | -84 | true |
| tokenBased | 13 | 71 | -58 | true |
| treeBased | 6 | 25 | -19 | false |

```json
{
  "total": 215,
  "replacement_api": "scipy.optimize._basinhopping.basinhopping",
  "threshold_10pct": 21.5,
  "vi_minus_1": {
    "mapBased": {
      "rank": 5,
      "score": 0.410533
    },
    "tokenBased": {
      "rank": 13,
      "score": 0.501119
    },
    "treeBased": {
      "rank": 6,
      "score": 0.433471
    }
  },
  "vi": {
    "mapBased": {
      "rank": 89,
      "score": 0.251723
    },
    "tokenBased": {
      "rank": 71,
      "score": 0.230519
    },
    "treeBased": {
      "rank": 25,
      "score": 0.395881
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 5,
      "vi_rank": 89,
      "delta": -84,
      "exceeds_10pct": true
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 13,
      "vi_rank": 71,
      "delta": -58,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 6,
      "vi_rank": 25,
      "delta": -19,
      "exceeds_10pct": false
    }
  ]
}
```

# 二、old → new Diff

- **old**: `scipy.optimize.anneal.anneal/Vi-1_v0.10.1.py`
- **new**: `scipy.optimize.anneal.anneal/Vi_v0.11.0.py`
- **+21 / -76**

```diff
--- scipy.optimize.anneal.anneal/Vi-1_v0.10.1.py
+++ scipy.optimize.anneal.anneal/Vi_v0.11.0.py
@@ -9,85 +9,30 @@
 def anneal(func, x0, args=(), schedule='fast', full_output=0,
            T0=None, Tf=1e-12, maxeval=None, maxaccept=None, maxiter=400,
            boltzmann=1.0, learn_rate=0.5, feps=1e-6, quench=1.0, m=1.0, n=1.0,
-           lower=-100, upper=100, dwell=50):
+           lower=-100, upper=100, dwell=50, disp=True):
     
-    x0 = asarray(x0)
-    lower = asarray(lower)
-    upper = asarray(upper)
 
-    schedule = eval(schedule+'_sa()')
+    opts = {'schedule'  : schedule,
+            'T0'        : T0,
+            'Tf'        : Tf,
+            'maxfev'    : maxeval,
+            'maxaccept' : maxaccept,
+            'maxiter'   : maxiter,
+            'boltzmann' : boltzmann,
+            'learn_rate': learn_rate,
+            'ftol'      : feps,
+            'quench'    : quench,
+            'm'         : m,
+            'n'         : n,
+            'lower'     : lower,
+            'upper'     : upper,
+            'dwell'     : dwell,
+            'disp'      : disp}
 
-    schedule.init(dims=shape(x0),func=func,args=args,boltzmann=boltzmann,T0=T0,
-                  learn_rate=learn_rate, lower=lower, upper=upper,
-                  m=m, n=n, quench=quench, dwell=dwell)
-
-    current_state, last_state, best_state = _state(), _state(), _state()
-    if T0 is None:
-        x0 = schedule.getstart_temp(best_state)
-    else:
-        best_state.x = None
-        best_state.cost = numpy.Inf
-
-    last_state.x = asarray(x0).copy()
-    fval = func(x0,*args)
-    schedule.feval += 1
-    last_state.cost = fval
-    if last_state.cost < best_state.cost:
-        best_state.cost = fval
-        best_state.x = asarray(x0).copy()
-    schedule.T = schedule.T0
-    fqueue = [100, 300, 500, 700]
-    iters = 0
-    while 1:
-        for n in xrange(dwell):
-            current_state.x = schedule.update_guess(last_state.x)
-            current_state.cost = func(current_state.x,*args)
-            schedule.feval += 1
-
-            dE = current_state.cost - last_state.cost
-            if schedule.accept_test(dE):
-                last_state.x = current_state.x.copy()
-                last_state.cost = current_state.cost
-                if last_state.cost < best_state.cost:
-                    best_state.x = last_state.x.copy()
-                    best_state.cost = last_state.cost
-        schedule.update_temp()
-        iters += 1
-
-
-
-
-
-
-
-
-        fqueue.append(squeeze(last_state.cost))
-        fqueue.pop(0)
-        af = asarray(fqueue)*1.0
-        if all(abs((af-af[0])/af[0]) < feps):
-            retval = 0
-            if abs(af[-1]-best_state.cost) > feps*10:
-                retval = 5
-                print "Warning: Cooled to %f at %s but this is not" \
-                      % (squeeze(last_state.cost), str(squeeze(last_state.x))) \
-                      + " the smallest point found."
-            break
-        if (Tf is not None) and (schedule.T < Tf):
-            retval = 1
-            break
-        if (maxeval is not None) and (schedule.feval > maxeval):
-            retval = 2
-            break
-        if (iters > maxiter):
-            print "Warning: Maximum number of iterations exceeded."
-            retval = 3
-            break
-        if (maxaccept is not None) and (schedule.accepted > maxaccept):
-            retval = 4
-            break
+    res = _minimize_anneal(func, x0, args, **opts)
 
     if full_output:
-        return best_state.x, best_state.cost, schedule.T, \
-               schedule.feval, iters, schedule.accepted, retval
+        return res['x'], res['fun'], res['T'], res['nfev'], res['nit'], \
+            res['accept'], res['status']
     else:
-        return best_state.x, retval
+        return res['x'], res['status']
```

```json
{
  "old_file": "scipy.optimize.anneal.anneal/Vi-1_v0.10.1.py",
  "new_file": "scipy.optimize.anneal.anneal/Vi_v0.11.0.py",
  "lines_added": 21,
  "lines_removed": 76
}
```
