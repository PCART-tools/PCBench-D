    def _formatter(self, boxed=False):
        def fmt(x):
            if isna(x):
                return 'NaN'
            return str(x)
        return fmt
