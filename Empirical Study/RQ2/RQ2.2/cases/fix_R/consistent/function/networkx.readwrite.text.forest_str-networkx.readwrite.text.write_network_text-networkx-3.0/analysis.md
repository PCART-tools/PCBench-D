# 一、突变情况分析

- **Total**: 127
- **替代API**: `networkx.readwrite.text.write_network_text`
- **10% 阈值**: 12.7

## Vi-1 (networkx-3.0-networkx-3.4)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 30 | 0.1667 |
| tokenBased | 59 | 0.1658 |
| treeBased | 45 | 0.2276 |

## Vi (networkx-3.1-networkx-3.4)

| 算法 | rank | score |
|------|------|-------|
| mapBased | 18 | 0.4646 |
| tokenBased | 1 | 0.5333 |
| treeBased | 1 | 0.5222 |

## Vi-1 → Vi 变化

| 算法 | Vi-1 rank | Vi rank | Δ | exceeds_10_percent |
|------|-----------|---------|---|--------------------|
| mapBased | 30 | 18 | +12 | false |
| tokenBased | 59 | 1 | +58 | true |
| treeBased | 45 | 1 | +44 | true |

```json
{
  "total": 127,
  "replacement_api": "networkx.readwrite.text.write_network_text",
  "threshold_10pct": 12.7,
  "vi_minus_1": {
    "mapBased": {
      "rank": 30,
      "score": 0.166667
    },
    "tokenBased": {
      "rank": 59,
      "score": 0.165761
    },
    "treeBased": {
      "rank": 45,
      "score": 0.227642
    }
  },
  "vi": {
    "mapBased": {
      "rank": 18,
      "score": 0.464574
    },
    "tokenBased": {
      "rank": 1,
      "score": 0.533333
    },
    "treeBased": {
      "rank": 1,
      "score": 0.522222
    }
  },
  "delta": [
    {
      "algorithm": "mapBased",
      "vi1_rank": 30,
      "vi_rank": 18,
      "delta": 12,
      "exceeds_10pct": false
    },
    {
      "algorithm": "tokenBased",
      "vi1_rank": 59,
      "vi_rank": 1,
      "delta": 58,
      "exceeds_10pct": true
    },
    {
      "algorithm": "treeBased",
      "vi1_rank": 45,
      "vi_rank": 1,
      "delta": 44,
      "exceeds_10pct": true
    }
  ]
}
```

# 二、old → new Diff

- **old**: `networkx.readwrite.text.forest_str/Vi-1_networkx-3.0.py`
- **new**: `networkx.readwrite.text.forest_str/Vi_networkx-3.1.py`
- **+18 / -109**

```diff
--- networkx.readwrite.text.forest_str/Vi-1_networkx-3.0.py
+++ networkx.readwrite.text.forest_str/Vi_networkx-3.1.py
@@ -1,6 +1,15 @@
 def forest_str(graph, with_labels=True, sources=None, write=None, ascii_only=False):
     
-    import networkx as nx
+    msg = (
+        "\nforest_str is deprecated as of version 3.1 and will be removed "
+        "in version 3.3. Use generate_network_text or write_network_text "
+        "instead.\n"
+    )
+    warnings.warn(msg, DeprecationWarning)
+
+    if len(graph.nodes) > 0:
+        if not nx.is_forest(graph):
+            raise nx.NetworkXNotImplemented("input must be a forest or the empty graph")
 
     printbuf = []
     if write is None:
@@ -8,114 +17,14 @@
     else:
         _write = write
 
-
-
-
-
-    if ascii_only:
-        glyph_empty = "+"
-        glyph_newtree_last = "+-- "
-        glyph_newtree_mid = "+-- "
-        glyph_endof_forest = "    "
-        glyph_within_forest = ":   "
-        glyph_within_tree = "|   "
-
-        glyph_directed_last = "L-> "
-        glyph_directed_mid = "|-> "
-
-        glyph_undirected_last = "L-- "
-        glyph_undirected_mid = "|-- "
-    else:
-        glyph_empty = "╙"
-        glyph_newtree_last = "╙── "
-        glyph_newtree_mid = "╟── "
-        glyph_endof_forest = "    "
-        glyph_within_forest = "╎   "
-        glyph_within_tree = "│   "
-
-        glyph_directed_last = "└─╼ "
-        glyph_directed_mid = "├─╼ "
-
-        glyph_undirected_last = "└── "
-        glyph_undirected_mid = "├── "
-
-    if len(graph.nodes) == 0:
-        _write(glyph_empty)
-    else:
-        if not nx.is_forest(graph):
-            raise nx.NetworkXNotImplemented("input must be a forest or the empty graph")
-
-        is_directed = graph.is_directed()
-        succ = graph.succ if is_directed else graph.adj
-
-        if sources is None:
-            if is_directed:
-
-                sources = [n for n in graph.nodes if graph.in_degree[n] == 0]
-            else:
-
-                sources = [
-                    min(cc, key=lambda n: graph.degree[n])
-                    for cc in nx.connected_components(graph)
-                ]
-
-
-
-
-        last_idx = len(sources) - 1
-        stack = [(node, "", (idx == last_idx)) for idx, node in enumerate(sources)][
-            ::-1
-        ]
-
-        seen = set()
-        while stack:
-            node, indent, islast = stack.pop()
-            if node in seen:
-                continue
-            seen.add(node)
-
-            if not indent:
-
-
-                if islast:
-                    this_prefix = indent + glyph_newtree_last
-                    next_prefix = indent + glyph_endof_forest
-                else:
-                    this_prefix = indent + glyph_newtree_mid
-                    next_prefix = indent + glyph_within_forest
-
-            else:
-
-
-                if is_directed:
-                    if islast:
-                        this_prefix = indent + glyph_directed_last
-                        next_prefix = indent + glyph_endof_forest
-                    else:
-                        this_prefix = indent + glyph_directed_mid
-                        next_prefix = indent + glyph_within_tree
-                else:
-                    if islast:
-                        this_prefix = indent + glyph_undirected_last
-                        next_prefix = indent + glyph_endof_forest
-                    else:
-                        this_prefix = indent + glyph_undirected_mid
-                        next_prefix = indent + glyph_within_tree
-
-            if with_labels:
-                label = graph.nodes[node].get("label", node)
-            else:
-                label = node
-
-            _write(this_prefix + str(label))
-
-
-
-            children = [child for child in succ[node] if child not in seen]
-            for idx, child in enumerate(children[::-1], start=1):
-                islast_next = idx <= 1
-                try_frame = (child, next_prefix, islast_next)
-                stack.append(try_frame)
+    write_network_text(
+        graph,
+        _write,
+        with_labels=with_labels,
+        sources=sources,
+        ascii_only=ascii_only,
+        end="",
+    )
 
     if write is None:
 
```

```json
{
  "old_file": "networkx.readwrite.text.forest_str/Vi-1_networkx-3.0.py",
  "new_file": "networkx.readwrite.text.forest_str/Vi_networkx-3.1.py",
  "lines_added": 18,
  "lines_removed": 109
}
```
