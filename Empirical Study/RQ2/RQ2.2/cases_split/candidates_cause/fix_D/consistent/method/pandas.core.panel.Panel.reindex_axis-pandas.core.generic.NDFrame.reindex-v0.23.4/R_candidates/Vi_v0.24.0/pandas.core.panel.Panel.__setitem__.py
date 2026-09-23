    def __setitem__(self, key, value):
        key = com.apply_if_callable(key, self)
        shape = tuple(self.shape)
        if isinstance(value, self._constructor_sliced):
            value = value.reindex(
                **self._construct_axes_dict_for_slice(self._AXIS_ORDERS[1:]))
            mat = value.values
        elif isinstance(value, np.ndarray):
            if value.shape != shape[1:]:
                raise ValueError('shape of value must be {0}, shape of given '
                                 'object was {1}'.format(
                                     shape[1:], tuple(map(int, value.shape))))
            mat = np.asarray(value)
        elif is_scalar(value):
            mat = cast_scalar_to_array(shape[1:], value)
        else:
            raise TypeError('Cannot set item of '
                            'type: {dtype!s}'.format(dtype=type(value)))

        mat = mat.reshape(tuple([1]) + shape[1:])
        NDFrame._set_item(self, key, mat)
