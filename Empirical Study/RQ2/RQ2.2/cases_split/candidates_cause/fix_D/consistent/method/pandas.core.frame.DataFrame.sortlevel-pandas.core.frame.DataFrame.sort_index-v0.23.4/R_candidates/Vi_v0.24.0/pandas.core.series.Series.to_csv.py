    @Appender(generic.NDFrame.to_csv.__doc__)
    def to_csv(self, *args, **kwargs):

        names = ["path_or_buf", "sep", "na_rep", "float_format", "columns",
                 "header", "index", "index_label", "mode", "encoding",
                 "compression", "quoting", "quotechar", "line_terminator",
                 "chunksize", "tupleize_cols", "date_format", "doublequote",
                 "escapechar", "decimal"]

        old_names = ["path_or_buf", "index", "sep", "na_rep", "float_format",
                     "header", "index_label", "mode", "encoding",
                     "compression", "date_format", "decimal"]

        if "path" in kwargs:
            warnings.warn("The signature of `Series.to_csv` was aligned "
                          "to that of `DataFrame.to_csv`, and argument "
                          "'path' will be renamed to 'path_or_buf'.",
                          FutureWarning, stacklevel=2)
            kwargs["path_or_buf"] = kwargs.pop("path")

        if len(args) > 1:
            # Either "index" (old signature) or "sep" (new signature) is being
            # passed as second argument (while the first is the same)
            maybe_sep = args[1]

            if not (is_string_like(maybe_sep) and len(maybe_sep) == 1):
                # old signature
                warnings.warn("The signature of `Series.to_csv` was aligned "
                              "to that of `DataFrame.to_csv`. Note that the "
                              "order of arguments changed, and the new one "
                              "has 'sep' in first place, for which \"{}\" is "
                              "not a valid value. The old order will cease to "
                              "be supported in a future version. Please refer "
                              "to the documentation for `DataFrame.to_csv` "
                              "when updating your function "
                              "calls.".format(maybe_sep),
                              FutureWarning, stacklevel=2)
                names = old_names

        pos_args = dict(zip(names[:len(args)], args))

        for key in pos_args:
            if key in kwargs:
                raise ValueError("Argument given by name ('{}') and position "
                                 "({})".format(key, names.index(key)))
            kwargs[key] = pos_args[key]

        if kwargs.get("header", None) is None:
            warnings.warn("The signature of `Series.to_csv` was aligned "
                          "to that of `DataFrame.to_csv`, and argument "
                          "'header' will change its default value from False "
                          "to True: please pass an explicit value to suppress "
                          "this warning.", FutureWarning,
                          stacklevel=2)
            kwargs["header"] = False  # Backwards compatibility.
        return self.to_frame().to_csv(**kwargs)
