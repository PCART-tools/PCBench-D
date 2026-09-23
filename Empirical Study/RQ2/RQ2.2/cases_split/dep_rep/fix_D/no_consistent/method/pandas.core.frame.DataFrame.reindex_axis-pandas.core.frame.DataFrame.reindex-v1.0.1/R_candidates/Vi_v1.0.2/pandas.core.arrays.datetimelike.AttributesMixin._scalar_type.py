    @property
    def _scalar_type(self) -> Type[DatetimeLikeScalar]:
        """The scalar associated with this datelike

        * PeriodArray : Period
        * DatetimeArray : Timestamp
        * TimedeltaArray : Timedelta
        """
        raise AbstractMethodError(self)
