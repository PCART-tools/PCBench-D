    def _box_item_values(self, key, values):
        if self.ndim == values.ndim:
            result = self._constructor(values)

            # a dup selection will yield a full ndim
            if result._get_axis(0).is_unique:
                result = result[key]

            return result

        d = self._construct_axes_dict_for_slice(self._AXIS_ORDERS[1:])
        return self._constructor_sliced(values, **d)
