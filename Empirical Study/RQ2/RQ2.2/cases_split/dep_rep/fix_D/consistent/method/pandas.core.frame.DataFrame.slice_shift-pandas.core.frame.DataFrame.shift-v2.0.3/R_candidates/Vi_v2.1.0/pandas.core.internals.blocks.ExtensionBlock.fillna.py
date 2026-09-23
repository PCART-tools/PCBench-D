    def fillna(
        self,
        value,
        limit: int | None = None,
        inplace: bool = False,
        downcast=None,
        using_cow: bool = False,
    ) -> list[Block]:
        if isinstance(self.dtype, IntervalDtype):
            # Block.fillna handles coercion (test_fillna_interval)
            return super().fillna(
                value=value,
                limit=limit,
                inplace=inplace,
                downcast=downcast,
                using_cow=using_cow,
            )
        if using_cow and self._can_hold_na and not self.values._hasna:
            refs = self.refs
            new_values = self.values
        else:
            copy, refs = self._get_refs_and_copy(using_cow, inplace)

            try:
                new_values = self.values.fillna(
                    value=value, method=None, limit=limit, copy=copy
                )
            except TypeError:
                # 3rd party EA that has not implemented copy keyword yet
                refs = None
                new_values = self.values.fillna(value=value, method=None, limit=limit)
                # issue the warning *after* retrying, in case the TypeError
                #  was caused by an invalid fill_value
                warnings.warn(
                    # GH#53278
                    "ExtensionArray.fillna added a 'copy' keyword in pandas "
                    "2.1.0. In a future version, ExtensionArray subclasses will "
                    "need to implement this keyword or an exception will be "
                    "raised. In the interim, the keyword is ignored by "
                    f"{type(self.values).__name__}.",
                    DeprecationWarning,
                    stacklevel=find_stack_level(),
                )

        nb = self.make_block_same_class(new_values, refs=refs)
        return nb._maybe_downcast([nb], downcast, using_cow=using_cow)
