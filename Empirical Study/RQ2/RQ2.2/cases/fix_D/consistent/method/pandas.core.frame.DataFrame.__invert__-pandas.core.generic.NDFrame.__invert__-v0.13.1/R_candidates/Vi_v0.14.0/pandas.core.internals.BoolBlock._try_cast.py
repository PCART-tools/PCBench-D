    def _try_cast(self, element):
        try:
            return bool(element)
        except:  # pragma: no cover
            return element
