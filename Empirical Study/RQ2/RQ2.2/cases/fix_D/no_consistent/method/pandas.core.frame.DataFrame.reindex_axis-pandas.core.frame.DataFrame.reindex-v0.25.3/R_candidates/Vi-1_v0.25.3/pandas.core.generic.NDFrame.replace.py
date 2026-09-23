    @Appender(_shared_docs["replace"] % _shared_doc_kwargs)
    def replace(
        self,
        to_replace=None,
        value=None,
        inplace=False,
        limit=None,
        regex=False,
        method="pad",
    ):
        inplace = validate_bool_kwarg(inplace, "inplace")
        if not is_bool(regex) and to_replace is not None:
            raise AssertionError(
                "'to_replace' must be 'None' if 'regex' is " "not a bool"
            )

        self._consolidate_inplace()

        if value is None:
            # passing a single value that is scalar like
            # when value is None (GH5319), for compat
            if not is_dict_like(to_replace) and not is_dict_like(regex):
                to_replace = [to_replace]

            if isinstance(to_replace, (tuple, list)):
                if isinstance(self, pd.DataFrame):
                    return self.apply(
                        _single_replace, args=(to_replace, method, inplace, limit)
                    )
                return _single_replace(self, to_replace, method, inplace, limit)

            if not is_dict_like(to_replace):
                if not is_dict_like(regex):
                    raise TypeError(
                        'If "to_replace" and "value" are both None'
                        ' and "to_replace" is not a list, then '
                        "regex must be a mapping"
                    )
                to_replace = regex
                regex = True

            items = list(to_replace.items())
            keys, values = zip(*items) if items else ([], [])

            are_mappings = [is_dict_like(v) for v in values]

            if any(are_mappings):
                if not all(are_mappings):
                    raise TypeError(
                        "If a nested mapping is passed, all values"
                        " of the top level mapping must be "
                        "mappings"
                    )
                # passed a nested dict/Series
                to_rep_dict = {}
                value_dict = {}

                for k, v in items:
                    keys, values = list(zip(*v.items())) or ([], [])
                    if set(keys) & set(values):
                        raise ValueError(
                            "Replacement not allowed with "
                            "overlapping keys and values"
                        )
                    to_rep_dict[k] = list(keys)
                    value_dict[k] = list(values)

                to_replace, value = to_rep_dict, value_dict
            else:
                to_replace, value = keys, values

            return self.replace(
                to_replace, value, inplace=inplace, limit=limit, regex=regex
            )
        else:

            # need a non-zero len on all axes
            if not self.size:
                return self

            new_data = self._data
            if is_dict_like(to_replace):
                if is_dict_like(value):  # {'A' : NA} -> {'A' : 0}
                    res = self if inplace else self.copy()
                    for c, src in to_replace.items():
                        if c in value and c in self:
                            # object conversion is handled in
                            # series.replace which is called recursively
                            res[c] = res[c].replace(
                                to_replace=src,
                                value=value[c],
                                inplace=False,
                                regex=regex,
                            )
                    return None if inplace else res

                # {'A': NA} -> 0
                elif not is_list_like(value):
                    keys = [(k, src) for k, src in to_replace.items() if k in self]
                    keys_len = len(keys) - 1
                    for i, (k, src) in enumerate(keys):
                        convert = i == keys_len
                        new_data = new_data.replace(
                            to_replace=src,
                            value=value,
                            filter=[k],
                            inplace=inplace,
                            regex=regex,
                            convert=convert,
                        )
                else:
                    raise TypeError("value argument must be scalar, dict, or " "Series")

            elif is_list_like(to_replace):  # [NA, ''] -> [0, 'missing']
                if is_list_like(value):
                    if len(to_replace) != len(value):
                        raise ValueError(
                            "Replacement lists must match "
                            "in length. Expecting %d got %d "
                            % (len(to_replace), len(value))
                        )

                    new_data = self._data.replace_list(
                        src_list=to_replace,
                        dest_list=value,
                        inplace=inplace,
                        regex=regex,
                    )

                else:  # [NA, ''] -> 0
                    new_data = self._data.replace(
                        to_replace=to_replace, value=value, inplace=inplace, regex=regex
                    )
            elif to_replace is None:
                if not (
                    is_re_compilable(regex)
                    or is_list_like(regex)
                    or is_dict_like(regex)
                ):
                    raise TypeError(
                        "'regex' must be a string or a compiled "
                        "regular expression or a list or dict of "
                        "strings or regular expressions, you "
                        "passed a"
                        " {0!r}".format(type(regex).__name__)
                    )
                return self.replace(
                    regex, value, inplace=inplace, limit=limit, regex=True
                )
            else:

                # dest iterable dict-like
                if is_dict_like(value):  # NA -> {'A' : 0, 'B' : -1}
                    new_data = self._data

                    for k, v in value.items():
                        if k in self:
                            new_data = new_data.replace(
                                to_replace=to_replace,
                                value=v,
                                filter=[k],
                                inplace=inplace,
                                regex=regex,
                            )

                elif not is_list_like(value):  # NA -> 0
                    new_data = self._data.replace(
                        to_replace=to_replace, value=value, inplace=inplace, regex=regex
                    )
                else:
                    msg = ('Invalid "to_replace" type: ' "{0!r}").format(
                        type(to_replace).__name__
                    )
                    raise TypeError(msg)  # pragma: no cover

        if inplace:
            self._update_inplace(new_data)
        else:
            return self._constructor(new_data).__finalize__(self)
