    @property
    def series_generator(self):
        values = self.values
        values = ensure_wrapped_if_datetimelike(values)
        assert len(values) > 0

        # We create one Series object, and will swap out the data inside
        #  of it.  Kids: don't do this at home.
        ser = self.obj._ixs(0, axis=0)
        mgr = ser._mgr

        if is_extension_array_dtype(ser.dtype):
            # values will be incorrect for this block
            # TODO(EA2D): special case would be unnecessary with 2D EAs
            obj = self.obj
            for i in range(len(obj)):
                yield obj._ixs(i, axis=0)

        else:
            for (arr, name) in zip(values, self.index):
                # GH#35462 re-pin mgr in case setitem changed it
                ser._mgr = mgr
                mgr.set_values(arr)
                ser.name = name
                yield ser
