    def agg_series(self, obj, func):
        dummy = obj[:0]
        grouper = lib.SeriesBinGrouper(obj, func, self.bins, dummy)
        return grouper.get_result()
