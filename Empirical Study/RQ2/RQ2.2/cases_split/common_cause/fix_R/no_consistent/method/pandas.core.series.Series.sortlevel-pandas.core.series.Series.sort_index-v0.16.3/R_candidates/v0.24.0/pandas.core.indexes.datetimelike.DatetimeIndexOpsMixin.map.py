    def map(self, f):
        try:
            result = f(self)

            # Try to use this result if we can
            if isinstance(result, np.ndarray):
                result = Index(result)

            if not isinstance(result, Index):
                raise TypeError('The map function must return an Index object')
            return result
        except Exception:
            return self.astype(object).map(f)
