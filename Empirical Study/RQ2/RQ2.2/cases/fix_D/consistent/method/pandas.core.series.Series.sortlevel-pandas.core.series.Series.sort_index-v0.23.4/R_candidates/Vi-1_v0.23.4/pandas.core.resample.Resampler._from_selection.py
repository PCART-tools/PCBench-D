    @property
    def _from_selection(self):
        """ is the resampling from a DataFrame column or MultiIndex level """
        # upsampling and PeriodIndex resampling do not work
        # with selection, this state used to catch and raise an error
        return (self.groupby is not None and
                (self.groupby.key is not None or
                 self.groupby.level is not None))
