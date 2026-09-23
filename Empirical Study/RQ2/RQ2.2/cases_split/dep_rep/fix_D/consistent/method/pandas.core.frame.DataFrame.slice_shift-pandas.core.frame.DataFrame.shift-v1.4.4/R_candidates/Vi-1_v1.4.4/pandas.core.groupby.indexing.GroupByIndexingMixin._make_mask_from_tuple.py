    def _make_mask_from_tuple(self, args: tuple) -> bool | np.ndarray:
        mask: bool | np.ndarray = False

        for arg in args:
            if is_integer(arg):
                mask |= self._make_mask_from_int(cast(int, arg))
            elif isinstance(arg, slice):
                mask |= self._make_mask_from_slice(arg)
            else:
                raise ValueError(
                    f"Invalid argument {type(arg)}. Should be int or slice."
                )

        return mask
