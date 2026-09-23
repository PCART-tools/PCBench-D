    def _delegate_method(self, name, *args, **kwargs):
        from pandas import Series

        method = getattr(self.values, name)
        result = method(*args, **kwargs)

        if not is_list_like(result):
            return result

        result = Series(result, index=self.index, name=self.name)

        # setting this object will show a SettingWithCopyWarning/Error
        result.is_copy = ("modifications to a method of a datetimelike object "
                          "are not supported and are discarded. Change "
                          "values on the original.")

        return result
