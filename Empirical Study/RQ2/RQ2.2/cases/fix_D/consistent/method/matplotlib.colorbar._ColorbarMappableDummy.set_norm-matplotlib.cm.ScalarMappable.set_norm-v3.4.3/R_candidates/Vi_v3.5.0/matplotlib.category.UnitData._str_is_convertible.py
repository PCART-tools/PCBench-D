    @staticmethod
    def _str_is_convertible(val):
        """
        Helper method to check whether a string can be parsed as float or date.
        """
        try:
            float(val)
        except ValueError:
            try:
                dateutil.parser.parse(val)
            except (ValueError, TypeError):
                # TypeError if dateutil >= 2.8.1 else ValueError
                return False
        return True
