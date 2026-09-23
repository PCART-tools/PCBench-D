    def __arrow_array__(self, type=None):
        """
        Convert myself into a pyarrow Array.
        """
        import pyarrow

        from pandas.core.arrays.arrow.extension_types import ArrowIntervalType

        try:
            subtype = pyarrow.from_numpy_dtype(self.dtype.subtype)
        except TypeError as err:
            raise TypeError(
                f"Conversion to arrow with subtype '{self.dtype.subtype}' "
                "is not supported"
            ) from err
        interval_type = ArrowIntervalType(subtype, self.closed)
        storage_array = pyarrow.StructArray.from_arrays(
            [
                pyarrow.array(self._left, type=subtype, from_pandas=True),
                pyarrow.array(self._right, type=subtype, from_pandas=True),
            ],
            names=["left", "right"],
        )
        mask = self.isna()
        if mask.any():
            # if there are missing values, set validity bitmap also on the array level
            null_bitmap = pyarrow.array(~mask).buffers()[1]
            storage_array = pyarrow.StructArray.from_buffers(
                storage_array.type,
                len(storage_array),
                [null_bitmap],
                children=[storage_array.field(0), storage_array.field(1)],
            )

        if type is not None:
            if type.equals(interval_type.storage_type):
                return storage_array
            elif isinstance(type, ArrowIntervalType):
                # ensure we have the same subtype and closed attributes
                if not type.equals(interval_type):
                    raise TypeError(
                        "Not supported to convert IntervalArray to type with "
                        f"different 'subtype' ({self.dtype.subtype} vs {type.subtype}) "
                        f"and 'closed' ({self.closed} vs {type.closed}) attributes"
                    )
            else:
                raise TypeError(
                    f"Not supported to convert IntervalArray to '{type}' type"
                )

        return pyarrow.ExtensionArray.from_storage(interval_type, storage_array)
