    def apply_with_block(self: T, f, align_keys=None, swap_axis=True, **kwargs) -> T:
        # switch axis to follow BlockManager logic
        if swap_axis and "axis" in kwargs and self.ndim == 2:
            kwargs["axis"] = 1 if kwargs["axis"] == 0 else 0

        align_keys = align_keys or []
        aligned_args = {k: kwargs[k] for k in align_keys}

        result_arrays = []

        for i, arr in enumerate(self.arrays):

            if aligned_args:
                for k, obj in aligned_args.items():
                    if isinstance(obj, (ABCSeries, ABCDataFrame)):
                        # The caller is responsible for ensuring that
                        #  obj.axes[-1].equals(self.items)
                        if obj.ndim == 1:
                            if self.ndim == 2:
                                kwargs[k] = obj.iloc[slice(i, i + 1)]._values
                            else:
                                kwargs[k] = obj.iloc[:]._values
                        else:
                            kwargs[k] = obj.iloc[:, [i]]._values
                    else:
                        # otherwise we have an ndarray
                        if obj.ndim == 2:
                            kwargs[k] = obj[[i]]

            # error: Item "ExtensionArray" of "Union[Any, ExtensionArray]" has no
            # attribute "tz"
            if hasattr(arr, "tz") and arr.tz is None:  # type: ignore[union-attr]
                # DatetimeArray needs to be converted to ndarray for DatetimeLikeBlock

                # error: Item "ExtensionArray" of "Union[Any, ExtensionArray]" has no
                # attribute "_data"
                arr = arr._data  # type: ignore[union-attr]
            elif arr.dtype.kind == "m" and not isinstance(arr, np.ndarray):
                # TimedeltaArray needs to be converted to ndarray for TimedeltaBlock

                # error: "ExtensionArray" has no attribute "_data"
                arr = arr._data  # type: ignore[attr-defined]

            if self.ndim == 2:
                arr = ensure_block_shape(arr, 2)
                block = new_block(arr, placement=slice(0, 1, 1), ndim=2)
            else:
                block = new_block(arr, placement=slice(0, len(self), 1), ndim=1)

            applied = getattr(block, f)(**kwargs)
            if isinstance(applied, list):
                applied = applied[0]
            arr = applied.values
            if self.ndim == 2 and arr.ndim == 2:
                # 2D for np.ndarray or DatetimeArray/TimedeltaArray
                assert len(arr) == 1
                # error: No overload variant of "__getitem__" of "ExtensionArray"
                # matches argument type "Tuple[int, slice]"
                arr = arr[0, :]  # type: ignore[call-overload]
            result_arrays.append(arr)

        return type(self)(result_arrays, self._axes)
