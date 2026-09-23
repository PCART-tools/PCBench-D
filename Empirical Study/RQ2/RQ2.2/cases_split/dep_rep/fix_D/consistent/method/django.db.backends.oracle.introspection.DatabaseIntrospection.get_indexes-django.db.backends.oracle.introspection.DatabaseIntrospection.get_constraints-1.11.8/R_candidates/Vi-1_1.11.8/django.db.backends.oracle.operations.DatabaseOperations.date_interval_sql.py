    def date_interval_sql(self, timedelta):
        """
        NUMTODSINTERVAL converts number to INTERVAL DAY TO SECOND literal.
        """
        return "NUMTODSINTERVAL(%06f, 'SECOND')" % (timedelta.total_seconds()), []
