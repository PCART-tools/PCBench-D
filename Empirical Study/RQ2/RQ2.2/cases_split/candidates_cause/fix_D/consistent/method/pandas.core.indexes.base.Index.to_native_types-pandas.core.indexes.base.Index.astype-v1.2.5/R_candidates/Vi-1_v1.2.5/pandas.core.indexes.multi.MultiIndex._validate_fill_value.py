    def _validate_fill_value(self, item):
        if not isinstance(item, tuple):
            # Pad the key with empty strings if lower levels of the key
            # aren't specified:
            item = (item,) + ("",) * (self.nlevels - 1)
        elif len(item) != self.nlevels:
            raise ValueError("Item must have length equal to number of levels.")
        return item
