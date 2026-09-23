    def __getattr__(self, name):
        try:
            return self._dict[name]
        except KeyError:
            raise ValueError(
                f"'Spines' object does not contain a '{name}' spine")
