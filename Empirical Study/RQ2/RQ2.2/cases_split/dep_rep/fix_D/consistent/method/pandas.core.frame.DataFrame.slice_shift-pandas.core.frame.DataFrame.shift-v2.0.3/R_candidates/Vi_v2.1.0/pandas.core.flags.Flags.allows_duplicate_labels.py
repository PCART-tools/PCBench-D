    @allows_duplicate_labels.setter
    def allows_duplicate_labels(self, value: bool) -> None:
        value = bool(value)
        obj = self._obj()
        if obj is None:
            raise ValueError("This flag's object has been deleted.")

        if not value:
            for ax in obj.axes:
                ax._maybe_check_unique()

        self._allows_duplicate_labels = value
