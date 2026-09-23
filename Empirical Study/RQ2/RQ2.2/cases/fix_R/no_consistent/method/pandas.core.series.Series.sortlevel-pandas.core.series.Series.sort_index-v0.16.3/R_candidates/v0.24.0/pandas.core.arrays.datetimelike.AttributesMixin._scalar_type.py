    @property
    def _scalar_type(self):
        # type: () -> Union[type, Tuple[type]]
        """The scalar associated with this datelike

        * PeriodArray : Period
        * DatetimeArray : Timestamp
        * TimedeltaArray : Timedelta
        """
        raise AbstractMethodError(self)
