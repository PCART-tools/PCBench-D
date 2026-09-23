# 一、突变情况分析

- **Total**: 30
- **替代API**: `scipy.signal.windows.windows.dpss`
- **10% 阈值**: 3.0

## Vi-1 (v0.18.1-v1.1.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 20 | 0.3075 |
| tokenBased | 15 | 0.3303 |
| treeBased | 15 | 0.3558 |

## Vi (v0.19.0-v1.1.0)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 21 | 0.3460 |
| tokenBased | 17 | 0.2963 |
| treeBased | 18 | 0.3198 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 20 | 21 | -1 | false |
| tokenBased | 15 | 17 | -2 | false |
| treeBased | 15 | 18 | -3 | true |

```json
{
  "total": 30,
  "replacement_api": "scipy.signal.windows.windows.dpss",
  "threshold_10pct": 3.0,
  "vi_minus_1": {
    "mapBased": {
      "rank": 20,
      "score": 0.307463
    },
    "tokenBased": {
      "rank": 15,
      "score": 0.330296
    },
    "treeBased": {
      "rank": 15,
      "score": 0.355769
    }
  },
  "vi": {
    "mapBased": {
      "rank": 21,
      "score": 0.346003
    },
    "tokenBased": {
      "rank": 17,
      "score": 0.296296
    },
    "treeBased": {
      "rank": 18,
      "score": 0.319797
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 20,
      "vi_rank": 21,
      "delta": -1,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 15,
      "vi_rank": 17,
      "delta": -2,
      "exceeds_10pct": false
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 15,
      "vi_rank": 18,
      "delta": -3,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `scipy.signal.windows.slepian/Vi-1_v0.18.1.py`
- **new**: `scipy.signal.windows.slepian/Vi_v0.19.0.py`
- **+4 / -10**

```diff
--- scipy.signal.windows.slepian/Vi-1_v0.18.1.py
+++ scipy.signal.windows.slepian/Vi_v0.19.0.py
@@ -1,12 +1,8 @@
 def slepian(M, width, sym=True):
     
-    if M < 1:
-        return np.array([])
-    if M == 1:
-        return np.ones(1, 'd')
-    odd = M % 2
-    if not sym and not odd:
-        M = M + 1
+    if _len_guards(M):
+        return np.ones(M)
+    M, needs_trunc = _extend(M, sym)
 
 
     width = width / 2
@@ -20,6 +16,4 @@
     _, win = linalg.eig_banded(H, select='i', select_range=(M-1, M-1))
     win = win.ravel() / win.max()
 
-    if not sym and not odd:
-        win = win[:-1]
-    return win
+    return _truncate(win, needs_trunc)
```

```json
{
  "old_file": "scipy.signal.windows.slepian/Vi-1_v0.18.1.py",
  "new_file": "scipy.signal.windows.slepian/Vi_v0.19.0.py",
  "lines_added": 4,
  "lines_removed": 10
}
```
