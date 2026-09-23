    def replace(self, to_replace=None, value=None, inplace=False, limit=None,
                regex=False, method='pad', axis=None):
        """
        Replace values given in 'to_replace' with 'value'.

        Parameters
        ----------
        to_replace : str, regex, list, dict, Series, numeric, or None

            * str or regex:

                - str: string exactly matching `to_replace` will be replaced
                  with `value`
                - regex: regexs matching `to_replace` will be replaced with
                  `value`

            * list of str, regex, or numeric:

                - First, if `to_replace` and `value` are both lists, they
                  **must** be the same length.
                - Second, if ``regex=True`` then all of the strings in **both**
                  lists will be interpreted as regexs otherwise they will match
                  directly. This doesn't matter much for `value` since there
                  are only a few possible substitution regexes you can use.
                - str and regex rules apply as above.

            * dict:

                - Nested dictionaries, e.g., {'a': {'b': nan}}, are read as
                  follows: look in column 'a' for the value 'b' and replace it
                  with nan. You can nest regular expressions as well. Note that
                  column names (the top-level dictionary keys in a nested
                  dictionary) **cannot** be regular expressions.
                - Keys map to column names and values map to substitution
                  values. You can treat this as a special case of passing two
                  lists except that you are specifying the column to search in.

            * None:

                - This means that the ``regex`` argument must be a string,
                  compiled regular expression, or list, dict, ndarray or Series
                  of such elements. If `value` is also ``None`` then this
                  **must** be a nested dictionary or ``Series``.

            See the examples section for examples of each of these.
        value : scalar, dict, list, str, regex, default None
            Value to use to fill holes (e.g. 0), alternately a dict of values
            specifying which value to use for each column (columns not in the
            dict will not be filled). Regular expressions, strings and lists or
            dicts of such objects are also allowed.
        inplace : boolean, default False
            If True, in place. Note: this will modify any
            other views on this object (e.g. a column form a DataFrame).
            Returns the caller if this is True.
        limit : int, default None
            Maximum size gap to forward or backward fill
        regex : bool or same types as `to_replace`, default False
            Whether to interpret `to_replace` and/or `value` as regular
            expressions. If this is ``True`` then `to_replace` *must* be a
            string. Otherwise, `to_replace` must be ``None`` because this
            parameter will be interpreted as a regular expression or a list,
            dict, or array of regular expressions.
        method : string, optional, {'pad', 'ffill', 'bfill'}
            The method to use when for replacement, when ``to_replace`` is a
            ``list``.

        See also
        --------
        NDFrame.reindex
        NDFrame.asfreq
        NDFrame.fillna

        Returns
        -------
        filled : NDFrame

        Raises
        ------
        AssertionError
            * If `regex` is not a ``bool`` and `to_replace` is not ``None``.
        TypeError
            * If `to_replace` is a ``dict`` and `value` is not a ``list``,
              ``dict``, ``ndarray``, or ``Series``
            * If `to_replace` is ``None`` and `regex` is not compilable into a
              regular expression or is a list, dict, ndarray, or Series.
        ValueError
            * If `to_replace` and `value` are ``list`` s or ``ndarray`` s, but
              they are not the same length.

        Notes
        -----
        * Regex substitution is performed under the hood with ``re.sub``. The
          rules for substitution for ``re.sub`` are the same.
        * Regular expressions will only substitute on strings, meaning you
          cannot provide, for example, a regular expression matching floating
          point numbers and expect the columns in your frame that have a
          numeric dtype to be matched. However, if those floating point numbers
          *are* strings, then you can do this.
        * This method has *a lot* of options. You are encouraged to experiment
          and play with this method to gain intuition about how it works.

        """
        if not com.is_bool(regex) and to_replace is not None:
            raise AssertionError("'to_replace' must be 'None' if 'regex' is "
                                 "not a bool")
        if axis is not None:
            from warnings import warn
            warn('the "axis" argument is deprecated and will be removed in'
                 'v0.13; this argument has no effect')

        self._consolidate_inplace()

        if value is None:
            # passing a single value that is scalar like
            # when value is None (GH5319), for compat
            if not is_dictlike(to_replace) and not is_dictlike(regex):
                to_replace = [to_replace]

            if isinstance(to_replace, (tuple, list)):
                return _single_replace(self, to_replace, method, inplace,
                                       limit)

            if not is_dictlike(to_replace):
                if not is_dictlike(regex):
                    raise TypeError('If "to_replace" and "value" are both None'
                                    ' and "to_replace" is not a list, then '
                                    'regex must be a mapping')
                to_replace = regex
                regex = True

            items = list(compat.iteritems(to_replace))
            keys, values = zip(*items)

            are_mappings = [is_dictlike(v) for v in values]

            if any(are_mappings):
                if not all(are_mappings):
                    raise TypeError("If a nested mapping is passed, all values"
                                    " of the top level mapping must be "
                                    "mappings")
                # passed a nested dict/Series
                to_rep_dict = {}
                value_dict = {}

                for k, v in items:
                    keys, values = zip(*v.items())
                    if set(keys) & set(values):
                        raise ValueError("Replacement not allowed with "
                                         "overlapping keys and values")
                    to_rep_dict[k] = list(keys)
                    value_dict[k] = list(values)

                to_replace, value = to_rep_dict, value_dict
            else:
                to_replace, value = keys, values

            return self.replace(to_replace, value, inplace=inplace,
                                limit=limit, regex=regex)
        else:

            # need a non-zero len on all axes
            for a in self._AXIS_ORDERS:
                if not len(self._get_axis(a)):
                    return self

            new_data = self._data
            if is_dictlike(to_replace):
                if is_dictlike(value):  # {'A' : NA} -> {'A' : 0}
                    res = self if inplace else self.copy()
                    for c, src in compat.iteritems(to_replace):
                        if c in value and c in self:
                            res[c] = res[c].replace(to_replace=src,
                                                    value=value[c],
                                                    inplace=False,
                                                    regex=regex)
                    return None if inplace else res

                # {'A': NA} -> 0
                elif not com.is_list_like(value):
                    for k, src in compat.iteritems(to_replace):
                        if k in self:
                            new_data = new_data.replace(to_replace=src,
                                                        value=value,
                                                        filter=[k],
                                                        inplace=inplace,
                                                        regex=regex)
                else:
                    raise TypeError('value argument must be scalar, dict, or '
                                    'Series')

            elif com.is_list_like(to_replace):  # [NA, ''] -> [0, 'missing']
                if com.is_list_like(value):
                    if len(to_replace) != len(value):
                        raise ValueError('Replacement lists must match '
                                         'in length. Expecting %d got %d ' %
                                         (len(to_replace), len(value)))

                    new_data = self._data.replace_list(src_list=to_replace,
                                                       dest_list=value,
                                                       inplace=inplace,
                                                       regex=regex)

                else:  # [NA, ''] -> 0
                    new_data = self._data.replace(to_replace=to_replace,
                                                  value=value,
                                                  inplace=inplace,
                                                  regex=regex)
            elif to_replace is None:
                if not (com.is_re_compilable(regex) or
                        com.is_list_like(regex) or
                        is_dictlike(regex)):
                    raise TypeError("'regex' must be a string or a compiled "
                                    "regular expression or a list or dict of "
                                    "strings or regular expressions, you "
                                    "passed a"
                                    " {0!r}".format(type(regex).__name__))
                return self.replace(regex, value, inplace=inplace, limit=limit,
                                    regex=True)
            else:

                # dest iterable dict-like
                if is_dictlike(value):  # NA -> {'A' : 0, 'B' : -1}
                    new_data = self._data

                    for k, v in compat.iteritems(value):
                        if k in self:
                            new_data = new_data.replace(to_replace=to_replace,
                                                        value=v,
                                                        filter=[k],
                                                        inplace=inplace,
                                                        regex=regex)

                elif not com.is_list_like(value):  # NA -> 0
                    new_data = self._data.replace(to_replace=to_replace, value=value,
                                                  inplace=inplace, regex=regex)
                else:
                    msg = ('Invalid "to_replace" type: '
                           '{0!r}').format(type(to_replace).__name__)
                    raise TypeError(msg)  # pragma: no cover

        new_data = new_data.convert(copy=not inplace, convert_numeric=False)

        if inplace:
            self._update_inplace(new_data)
        else:
            return self._constructor(new_data).__finalize__(self)
