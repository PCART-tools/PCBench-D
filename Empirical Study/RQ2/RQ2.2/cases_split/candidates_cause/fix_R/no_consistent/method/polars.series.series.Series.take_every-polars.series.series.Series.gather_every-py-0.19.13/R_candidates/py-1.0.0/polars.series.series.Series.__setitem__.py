    def __setitem__(
        self,
        key: int | Series | np.ndarray[Any, Any] | Sequence[object] | tuple[object],
        value: Any,
    ) -> None:
        # do the single idx as first branch as those are likely in a tight loop
        if isinstance(key, int) and not isinstance(key, bool):
            self.scatter(key, value)
            return None
        elif isinstance(value, Sequence) and not isinstance(value, str):
            if self.dtype.is_numeric() or self.dtype.is_temporal():
                self.scatter(key, value)  # type: ignore[arg-type]
                return None
            msg = (
                f"cannot set Series of dtype: {self.dtype!r} with list/tuple as value;"
                " use a scalar value"
            )
            raise TypeError(msg)
        if isinstance(key, Series):
            if key.dtype == Boolean:
                self._s = self.set(key, value)._s
            elif key.dtype == UInt64:
                self._s = self.scatter(key.cast(UInt32), value)._s
            elif key.dtype == UInt32:
                self._s = self.scatter(key, value)._s

        # TODO: implement for these types without casting to series
        elif _check_for_numpy(key) and isinstance(key, np.ndarray):
            if key.dtype == np.bool_:
                # boolean numpy mask
                self._s = self.scatter(np.argwhere(key)[:, 0], value)._s
            else:
                s = self._from_pyseries(
                    PySeries.new_u32("", np.array(key, np.uint32), _strict=True)
                )
                self.__setitem__(s, value)
        elif isinstance(key, (list, tuple)):
            s = self._from_pyseries(sequence_to_pyseries("", key, dtype=UInt32))
            self.__setitem__(s, value)
        else:
            msg = f'cannot use "{key!r}" for indexing'
            raise TypeError(msg)
