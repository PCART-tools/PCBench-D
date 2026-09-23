    @number.setter
    def number(self, num):
        _api.warn_deprecated(
            "3.10",
            message="Changing 'Figure.number' is deprecated since %(since)s and "
                    "will raise an error starting %(removal)s")
        self._number = num
