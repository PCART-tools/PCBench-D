    @final
    @doc(
        _shared_docs["replace"],
        klass=_shared_doc_kwargs["klass"],
        inplace=_shared_doc_kwargs["inplace"],
    )
    def replace(
        self,
        to_replace=None,
        value=lib.no_default,
        *,
        inplace: bool_t = False,
        limit: int | None = None,
        regex: bool_t = False,
        method: Literal["pad", "ffill", "bfill"] | lib.NoDefault = lib.no_default,
    ) -> Self | None:
        if method is not lib.no_default:
            warnings.warn(
                # GH#33302
                f"The 'method' keyword in {type(self).__name__}.replace is "
                "deprecated and will be removed in a future version.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
        elif limit is not None:
            warnings.warn(
                # GH#33302
                f"The 'limit' keyword in {type(self).__name__}.replace is "
                "deprecated and will be removed in a future version.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
        if (
            value is lib.no_default
            and method is lib.no_default
            and not is_dict_like(to_replace)
            and regex is False
        ):
            # case that goes through _replace_single and defaults to method="pad"
            warnings.warn(
                # GH#33302
                f"{type(self).__name__}.replace without 'value' and with "
                "non-dict-like 'to_replace' is deprecated "
                "and will raise in a future version. "
                "Explicitly specify the new values instead.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )

        if not (
            is_scalar(to_replace)
            or is_re_compilable(to_replace)
            or is_list_like(to_replace)
        ):
            raise TypeError(
                "Expecting 'to_replace' to be either a scalar, array-like, "
                "dict or None, got invalid type "
                f"{repr(type(to_replace).__name__)}"
            )

        inplace = validate_bool_kwarg(inplace, "inplace")
        if inplace:
            if not PYPY and using_copy_on_write():
                if sys.getrefcount(self) <= REF_COUNT:
                    warnings.warn(
                        _chained_assignment_method_msg,
                        ChainedAssignmentError,
                        stacklevel=2,
                    )

        if not is_bool(regex) and to_replace is not None:
            raise ValueError("'to_replace' must be 'None' if 'regex' is not a bool")

        if value is lib.no_default or method is not lib.no_default:
            # GH#36984 if the user explicitly passes value=None we want to
            #  respect that. We have the corner case where the user explicitly
            #  passes value=None *and* a method, which we interpret as meaning
            #  they want the (documented) default behavior.
            if method is lib.no_default:
                # TODO: get this to show up as the default in the docs?
                method = "pad"

            # passing a single value that is scalar like
            # when value is None (GH5319), for compat
            if not is_dict_like(to_replace) and not is_dict_like(regex):
                to_replace = [to_replace]

            if isinstance(to_replace, (tuple, list)):
                # TODO: Consider copy-on-write for non-replaced columns's here
                if isinstance(self, ABCDataFrame):
                    from pandas import Series

                    result = self.apply(
                        Series._replace_single,
                        args=(to_replace, method, inplace, limit),
                    )
                    if inplace:
                        return None
                    return result
                return self._replace_single(to_replace, method, inplace, limit)

            if not is_dict_like(to_replace):
                if not is_dict_like(regex):
                    raise TypeError(
                        'If "to_replace" and "value" are both None '
                        'and "to_replace" is not a list, then '
                        "regex must be a mapping"
                    )
                to_replace = regex
                regex = True

            items = list(to_replace.items())
            if items:
                keys, values = zip(*items)
            else:
                keys, values = ([], [])

            are_mappings = [is_dict_like(v) for v in values]

            if any(are_mappings):
                if not all(are_mappings):
                    raise TypeError(
                        "If a nested mapping is passed, all values "
                        "of the top level mapping must be mappings"
                    )
                # passed a nested dict/Series
                to_rep_dict = {}
                value_dict = {}

                for k, v in items:
                    keys, values = list(zip(*v.items())) or ([], [])

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
                if inplace:
                    return None
                return self.copy(deep=None)

            if is_dict_like(to_replace):
                if is_dict_like(value):  # {'A' : NA} -> {'A' : 0}
                    # Note: Checking below for `in foo.keys()` instead of
                    #  `in foo` is needed for when we have a Series and not dict
                    mapping = {
                        col: (to_replace[col], value[col])
                        for col in to_replace.keys()
                        if col in value.keys() and col in self
                    }
                    return self._replace_columnwise(mapping, inplace, regex)

                # {'A': NA} -> 0
                elif not is_list_like(value):
                    # Operate column-wise
                    if self.ndim == 1:
                        raise ValueError(
                            "Series.replace cannot use dict-like to_replace "
                            "and non-None value"
                        )
                    mapping = {
                        col: (to_rep, value) for col, to_rep in to_replace.items()
                    }
                    return self._replace_columnwise(mapping, inplace, regex)
                else:
                    raise TypeError("value argument must be scalar, dict, or Series")

            elif is_list_like(to_replace):
                if not is_list_like(value):
                    # e.g. to_replace = [NA, ''] and value is 0,
                    #  so we replace NA with 0 and then replace '' with 0
                    value = [value] * len(to_replace)

                # e.g. we have to_replace = [NA, ''] and value = [0, 'missing']
                if len(to_replace) != len(value):
                    raise ValueError(
                        f"Replacement lists must match in length. "
                        f"Expecting {len(to_replace)} got {len(value)} "
                    )
                new_data = self._mgr.replace_list(
                    src_list=to_replace,
                    dest_list=value,
                    inplace=inplace,
                    regex=regex,
                )

            elif to_replace is None:
                if not (
                    is_re_compilable(regex)
                    or is_list_like(regex)
                    or is_dict_like(regex)
                ):
                    raise TypeError(
                        f"'regex' must be a string or a compiled regular expression "
                        f"or a list or dict of strings or regular expressions, "
                        f"you passed a {repr(type(regex).__name__)}"
                    )
                return self.replace(
                    regex, value, inplace=inplace, limit=limit, regex=True
                )
            else:
                # dest iterable dict-like
                if is_dict_like(value):  # NA -> {'A' : 0, 'B' : -1}
                    # Operate column-wise
                    if self.ndim == 1:
                        raise ValueError(
                            "Series.replace cannot use dict-value and "
                            "non-None to_replace"
                        )
                    mapping = {col: (to_replace, val) for col, val in value.items()}
                    return self._replace_columnwise(mapping, inplace, regex)

                elif not is_list_like(value):  # NA -> 0
                    regex = should_use_regex(regex, to_replace)
                    if regex:
                        new_data = self._mgr.replace_regex(
                            to_replace=to_replace,
                            value=value,
                            inplace=inplace,
                        )
                    else:
                        new_data = self._mgr.replace(
                            to_replace=to_replace, value=value, inplace=inplace
                        )
                else:
                    raise TypeError(
                        f'Invalid "to_replace" type: {repr(type(to_replace).__name__)}'
                    )

        result = self._constructor_from_mgr(new_data, axes=new_data.axes)
        if inplace:
            return self._update_inplace(result)
        else:
            return result.__finalize__(self, method="replace")
