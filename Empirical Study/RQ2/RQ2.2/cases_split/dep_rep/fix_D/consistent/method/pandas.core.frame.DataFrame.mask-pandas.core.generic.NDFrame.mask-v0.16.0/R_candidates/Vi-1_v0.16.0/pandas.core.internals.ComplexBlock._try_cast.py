    def _try_cast(self, element):
        try:
            return complex(element)
        except:  # pragma: no cover
            return element
