# Diff 分块分析：sklearn.compose._column_transformer.ColumnTransformer.get_feature_names-sklearn.compose._column_transformer.ColumnTransformer.get_feature_names_out-0.22.2
## 文件定位

- 旧文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/sklearn.compose._column_transformer.ColumnTransformer.get_feature_names-sklearn.compose._column_transformer.ColumnTransformer.get_feature_names_out-0.22.2/sklearn.compose._column_transformer.ColumnTransformer.get_feature_names/Vi-1_0.22.2.py
- 新文件：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/sklearn.compose._column_transformer.ColumnTransformer.get_feature_names-sklearn.compose._column_transformer.ColumnTransformer.get_feature_names_out-0.22.2/sklearn.compose._column_transformer.ColumnTransformer.get_feature_names/Vi_0.23.0.py
- 目标文件（Target）：/media/he/Rbench/similarity/RQ2/split2.0/common_cause/fix_R/consistent/method/sklearn.compose._column_transformer.ColumnTransformer.get_feature_names-sklearn.compose._column_transformer.ColumnTransformer.get_feature_names_out-0.22.2/R_candidates/1.2.0/sklearn.compose._column_transformer.ColumnTransformer.get_feature_names_out.py
- 实验组：fix_R
- 总变更：+15 / -7 行
- 分块数：2

## Block 1 — block_001.patch
定位：@@ -10,4 +10,5 @@
说明：for name, trans, _, _ in self._iter(fitted=True):、if trans == 'drop':、for name, trans, column, _ in self._iter(fitted=True):...

## Block 2 — block_002.patch
定位：@@ -13,7 +14,14 @@
说明：elif trans == 'passthrough':、raise NotImplementedError(、"get_feature_names is not yet supported when using "...
