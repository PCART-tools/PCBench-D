    def _try_cast(self, element):
        try:
            return float(element)
        except:  # pragma: no cover
            return element
