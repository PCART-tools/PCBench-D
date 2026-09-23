    def agg_series(self, obj, func):
        try:
            return self._aggregate_series_fast(obj, func)
        except Exception:
            return self._aggregate_series_pure_python(obj, func)
