class _rcParam_helper:
    """
    This helper class is so that we can set the converter for dates
    via the validator for the rcParams `date.converter` and
    `date.interval_multiples`.  Never instatiated.
    """

    conv_st = 'auto'
    int_mult = True

    @classmethod
    def set_converter(cls, s):
        """Called by validator for rcParams date.converter"""
        if s not in ['concise', 'auto']:
            raise ValueError('Converter must be one of "concise" or "auto"')
        cls.conv_st = s
        cls.register_converters()

    @classmethod
    def set_int_mult(cls, b):
        """Called by validator for rcParams date.interval_multiples"""
        cls.int_mult = b
        cls.register_converters()

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
