    @property
    def is_all_dates(self):
        """
        This is False even when left/right contain datetime-like objects,
        as the check is done on the Interval itself
        """
        return False
