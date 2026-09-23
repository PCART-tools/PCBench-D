    def _addsub_object_array(self, other, op):
        # Add or subtract Array-like of objects
        try:
            # TimedeltaIndex can only operate with a subset of DateOffset
            # subclasses.  Incompatible classes will raise AttributeError,
            # which we re-raise as TypeError
            return super()._addsub_object_array(other, op)
        except AttributeError as err:
            raise TypeError(
                f"Cannot add/subtract non-tick DateOffset to {type(self).__name__}"
            ) from err
