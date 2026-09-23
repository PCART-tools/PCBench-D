    def __array_wrap__(self, result, context=None):
        """
        Gets called after a ufunc and other functions.
        """
        out = super().__array_wrap__(result, context=context)
        if isinstance(out, DatetimeTimedeltaMixin) and self.freq is not None:
            out = out._with_freq("infer")
        return out
