    @classmethod
    def set_converter(cls, s):
        """Called by validator for rcParams date.converter"""
        if s not in ['concise', 'auto']:
            raise ValueError('Converter must be one of "concise" or "auto"')
        cls.conv_st = s
        cls.register_converters()
