    def format_number(self, value):
        """
        Format a number into a string with the requisite number of digits and
        decimal places.
        """
        # Method moved to django.db.backends.utils.
        #
        # It is preserved because it is used by the oracle backend
        # (django.db.backends.oracle.query), and also for
        # backwards-compatibility with any external code which may have used
        # this method.
        from django.db.backends import utils
        return utils.format_number(value, self.max_digits, self.decimal_places)
