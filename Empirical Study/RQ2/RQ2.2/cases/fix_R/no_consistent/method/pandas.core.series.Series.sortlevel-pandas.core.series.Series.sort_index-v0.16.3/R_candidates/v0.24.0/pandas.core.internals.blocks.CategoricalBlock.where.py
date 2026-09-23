    def where(self, other, cond, align=True, errors='raise',
              try_cast=False, axis=0, transpose=False):
        # TODO(CategoricalBlock.where):
        # This can all be deleted in favor of ExtensionBlock.where once
        # we enforce the deprecation.
        object_msg = (
            "Implicitly converting categorical to object-dtype ndarray. "
            "One or more of the values in 'other' are not present in this "
            "categorical's categories. A future version of pandas will raise "
            "a ValueError when 'other' contains different categories.\n\n"
            "To preserve the current behavior, add the new categories to "
            "the categorical before calling 'where', or convert the "
            "categorical to a different dtype."
        )
        try:
            # Attempt to do preserve categorical dtype.
            result = super(CategoricalBlock, self).where(
                other, cond, align, errors, try_cast, axis, transpose
            )
        except (TypeError, ValueError):
            warnings.warn(object_msg, FutureWarning, stacklevel=6)
            result = self.astype(object).where(other, cond, align=align,
                                               errors=errors,
                                               try_cast=try_cast,
                                               axis=axis, transpose=transpose)
        return result
