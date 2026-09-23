    @staticmethod
    def _output_type_handler(cursor, name, defaultType, length, precision, scale):
        """
        Called for each db column fetched from cursors. Return numbers as
        strings so that decimal values don't have rounding error.
        """
        if defaultType == Database.NUMBER:
            return cursor.var(
                Database.STRING,
                size=255,
                arraysize=cursor.arraysize,
                outconverter=str,
            )
