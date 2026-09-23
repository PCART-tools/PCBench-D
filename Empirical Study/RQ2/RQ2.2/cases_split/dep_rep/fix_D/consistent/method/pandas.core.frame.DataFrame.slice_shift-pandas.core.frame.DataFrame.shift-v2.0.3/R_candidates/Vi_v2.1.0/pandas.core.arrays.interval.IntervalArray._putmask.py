    def _putmask(self, mask: npt.NDArray[np.bool_], value) -> None:
        value_left, value_right = self._validate_setitem_value(value)

        if isinstance(self._left, np.ndarray):
            np.putmask(self._left, mask, value_left)
            assert isinstance(self._right, np.ndarray)
            np.putmask(self._right, mask, value_right)
        else:
            self._left._putmask(mask, value_left)
            assert not isinstance(self._right, np.ndarray)
            self._right._putmask(mask, value_right)
