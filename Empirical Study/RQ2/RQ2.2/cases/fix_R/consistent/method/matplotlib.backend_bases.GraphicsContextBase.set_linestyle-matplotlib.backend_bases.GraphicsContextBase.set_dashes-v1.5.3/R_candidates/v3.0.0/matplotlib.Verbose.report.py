    @cbook.deprecated("2.2", message=_verbose_msg)
    def report(self, s, level='helpful'):
        """
        print message s to self.fileo if self.level>=level.  Return
        value indicates whether a message was issued

        """
        if self.ge(level):
            print(s, file=self.fileo)
            return True
        return False
