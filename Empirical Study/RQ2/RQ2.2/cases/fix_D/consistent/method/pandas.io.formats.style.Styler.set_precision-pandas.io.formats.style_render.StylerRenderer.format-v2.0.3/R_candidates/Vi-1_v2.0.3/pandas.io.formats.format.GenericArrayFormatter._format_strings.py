    def _format_strings(self) -> list[str]:
        if self.float_format is None:
            float_format = get_option("display.float_format")
            if float_format is None:
                precision = get_option("display.precision")
                float_format = lambda x: _trim_zeros_single_float(
                    f"{x: .{precision:d}f}"
                )
        else:
            float_format = self.float_format

        if self.formatter is not None:
            formatter = self.formatter
        elif self.fallback_formatter is not None:
            formatter = self.fallback_formatter
        else:
            quote_strings = self.quoting is not None and self.quoting != QUOTE_NONE
            formatter = partial(
                printing.pprint_thing,
                escape_chars=("\t", "\r", "\n"),
                quote_strings=quote_strings,
            )

        def _format(x):
            if self.na_rep is not None and is_scalar(x) and isna(x):
                try:
                    # try block for np.isnat specifically
                    # determine na_rep if x is None or NaT-like
                    if x is None:
                        return "None"
                    elif x is NA:
                        return str(NA)
                    elif x is NaT or np.isnat(x):
                        return "NaT"
                except (TypeError, ValueError):
                    # np.isnat only handles datetime or timedelta objects
                    pass
                return self.na_rep
            elif isinstance(x, PandasObject):
                return str(x)
            elif isinstance(x, StringDtype):
                return repr(x)
            else:
                # object dtype
                return str(formatter(x))

        vals = extract_array(self.values, extract_numpy=True)
        if not isinstance(vals, np.ndarray):
            raise TypeError(
                "ExtensionArray formatting should use ExtensionArrayFormatter"
            )
        inferred = lib.map_infer(vals, is_float)
        is_float_type = (
            inferred
            # vals may have 2 or more dimensions
            & np.all(notna(vals), axis=tuple(range(1, len(vals.shape))))
        )
        leading_space = self.leading_space
        if leading_space is None:
            leading_space = is_float_type.any()

        fmt_values = []
        for i, v in enumerate(vals):
            if (not is_float_type[i] or self.formatter is not None) and leading_space:
                fmt_values.append(f" {_format(v)}")
            elif is_float_type[i]:
                fmt_values.append(float_format(v))
            else:
                if leading_space is False:
                    # False specifically, so that the default is
                    # to include a space if we get here.
                    tpl = "{v}"
                else:
                    tpl = " {v}"
                fmt_values.append(tpl.format(v=_format(v)))

        return fmt_values
