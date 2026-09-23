    def _str_get_dummies(self, sep: str = "|"):
        split = pc.split_pattern(self._data, sep).combine_chunks()
        uniques = split.flatten().unique()
        uniques_sorted = uniques.take(pa.compute.array_sort_indices(uniques))
        result_data = []
        for lst in split.to_pylist():
            if lst is None:
                result_data.append([False] * len(uniques_sorted))
            else:
                res = pc.is_in(uniques_sorted, pa.array(set(lst)))
                result_data.append(res.to_pylist())
        result = type(self)(pa.array(result_data))
        return result, uniques_sorted.to_pylist()
