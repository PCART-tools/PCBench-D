    def _get_index_resolvers(self) -> Dict[str, ABCSeries]:
        from pandas.core.computation.parsing import clean_column_name

        d: Dict[str, ABCSeries] = {}
        for axis_name in self._AXIS_ORDERS:
            d.update(self._get_axis_resolvers(axis_name))

        return {clean_column_name(k): v for k, v in d.items() if not isinstance(k, int)}
