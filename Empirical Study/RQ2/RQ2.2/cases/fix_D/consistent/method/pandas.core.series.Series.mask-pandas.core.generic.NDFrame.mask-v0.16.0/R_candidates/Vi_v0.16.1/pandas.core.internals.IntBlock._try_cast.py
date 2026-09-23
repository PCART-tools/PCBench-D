    def _try_cast(self, element):
        try:
            return int(element)
        except:  # pragma: no cover
            return element
