    def _ensure_valid_index(self, value):
        """
        ensure that if we don't have an index, that we can create one from the
        passed value
        """
        if not len(self.index):

            # GH5632, make sure that we are a Series convertible
            if is_list_like(value):
                try:
                    value = Series(value)
                except:
                    pass

                if not isinstance(value, Series):
                    raise ValueError('Cannot set a frame with no defined index '
                                     'and a value that cannot be converted to a '
                                     'Series')
                self._data.set_axis(1, value.index.copy(), check_axis=False)

            # we are a scalar
            # noop
            else:

                pass
