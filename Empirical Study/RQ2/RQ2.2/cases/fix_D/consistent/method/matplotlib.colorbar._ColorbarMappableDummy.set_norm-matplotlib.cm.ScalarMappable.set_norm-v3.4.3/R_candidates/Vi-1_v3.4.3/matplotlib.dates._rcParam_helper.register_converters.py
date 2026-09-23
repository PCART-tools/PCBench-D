    @classmethod
    def register_converters(cls):
        """
        Helper to register the date converters when rcParams `date.converter`
        and `date.interval_multiples` are changed.  Called by the helpers
        above.
        """
        if cls.conv_st == 'concise':
            converter = ConciseDateConverter
        else:
            converter = DateConverter

        interval_multiples = cls.int_mult
        convert = converter(interval_multiples=interval_multiples)
        units.registry[np.datetime64] = convert
        units.registry[datetime.date] = convert
        units.registry[datetime.datetime] = convert
