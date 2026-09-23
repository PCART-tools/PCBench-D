    def _delegate_property_get(self, name):
        from pandas import Series

        result = getattr(self.values, name)

        # maybe need to upcast (ints)
        if isinstance(result, np.ndarray):
            if is_integer_dtype(result):
                result = result.astype('int64')
        elif not is_list_like(result):
            return result

        result = np.asarray(result)

        # blow up if we operate on categories
        if self.orig is not None:
            result = take_1d(result, self.orig.cat.codes)

        # return the result as a Series, which is by definition a copy
        result = Series(result, index=self.index, name=self.name)

        # setting this object will show a SettingWithCopyWarning/Error
        result.is_copy = ("modifications to a property of a datetimelike "
                          "object are not supported and are discarded. "
                          "Change values on the original.")

        return result
