    @staticmethod
    def convert(value, unit, axis):
        """
        Convert Decimals to floats.

        The *unit* and *axis* arguments are not used.

        Parameters
        ----------
        value : decimal.Decimal or iterable
            Decimal or list of Decimal need to be converted
        """
        # If value is a Decimal
        if isinstance(value, Decimal):
            return np.float(value)
        else:
            # assume x is a list of Decimal
            converter = np.asarray
            if isinstance(value, ma.MaskedArray):
                converter = ma.asarray
            return converter(value, dtype=np.float)
