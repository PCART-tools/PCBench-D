    def _replace_single(
        self,
        to_replace,
        value,
        inplace=False,
        filter=None,
        regex=False,
        convert=True,
        mask=None,
    ):
        """
        Replace elements by the given value.

        Parameters
        ----------
        to_replace : object or pattern
            Scalar to replace or regular expression to match.
        value : object
            Replacement object.
        inplace : bool, default False
            Perform inplace modification.
        filter : list, optional
        regex : bool, default False
            If true, perform regular expression substitution.
        convert : bool, default True
            If true, try to coerce any object types to better types.
        mask : array-like of bool, optional
            True indicate corresponding element is ignored.

        Returns
        -------
        a new block, the result after replacing
        """
        inplace = validate_bool_kwarg(inplace, "inplace")

        # to_replace is regex compilable
        to_rep_re = regex and is_re_compilable(to_replace)

        # regex is regex compilable
        regex_re = is_re_compilable(regex)

        # only one will survive
        if to_rep_re and regex_re:
            raise AssertionError(
                "only one of to_replace and regex can be regex compilable"
            )

        # if regex was passed as something that can be a regex (rather than a
        # boolean)
        if regex_re:
            to_replace = regex

        regex = regex_re or to_rep_re

        # try to get the pattern attribute (compiled re) or it's a string
        if is_re(to_replace):
            pattern = to_replace.pattern
        else:
            pattern = to_replace

        # if the pattern is not empty and to_replace is either a string or a
        # regex
        if regex and pattern:
            rx = re.compile(to_replace)
        else:
            # if the thing to replace is not a string or compiled regex call
            # the superclass method -> to_replace is some kind of object
            return super().replace(
                to_replace, value, inplace=inplace, filter=filter, regex=regex
            )

        new_values = self.values if inplace else self.values.copy()

        # deal with replacing values with objects (strings) that match but
        # whose replacement is not a string (numeric, nan, object)
        if isna(value) or not isinstance(value, str):

            def re_replacer(s):
                if is_re(rx) and isinstance(s, str):
                    return value if rx.search(s) is not None else s
                else:
                    return s

        else:
            # value is guaranteed to be a string here, s can be either a string
            # or null if it's null it gets returned
            def re_replacer(s):
                if is_re(rx) and isinstance(s, str):
                    return rx.sub(value, s)
                else:
                    return s

        f = np.vectorize(re_replacer, otypes=[self.dtype])

        if filter is None:
            filt = slice(None)
        else:
            filt = self.mgr_locs.isin(filter).nonzero()[0]

        if mask is None:
            new_values[filt] = f(new_values[filt])
        else:
            new_values[filt][mask] = f(new_values[filt][mask])

        # convert
        block = self.make_block(new_values)
        if convert:
            block = block.convert(numeric=False)
        return block
