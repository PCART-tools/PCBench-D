    @classmethod
    def set_int_mult(cls, b):
        """Called by validator for rcParams date.interval_multiples"""
        cls.int_mult = b
        cls.register_converters()
