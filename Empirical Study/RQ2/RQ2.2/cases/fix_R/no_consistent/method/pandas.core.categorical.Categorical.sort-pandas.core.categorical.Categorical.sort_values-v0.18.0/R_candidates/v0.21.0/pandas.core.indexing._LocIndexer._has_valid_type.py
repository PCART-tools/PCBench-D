    def _has_valid_type(self, key, axis):
        ax = self.obj._get_axis(axis)

        # valid for a label where all labels are in the index
        # slice of lables (where start-end in labels)
        # slice of integers (only if in the lables)
        # boolean

        if isinstance(key, slice):
            return True

        elif is_bool_indexer(key):
            return True

        elif is_list_like_indexer(key):

            # mi is just a passthru
            if isinstance(key, tuple) and isinstance(ax, MultiIndex):
                return True

            if not is_iterator(key) and len(key):

                # True indicates missing values
                missing = ax.get_indexer_for(key) < 0

                if np.any(missing):
                    if len(key) == 1 or np.all(missing):
                        raise KeyError(
                            u"None of [{key}] are in the [{axis}]".format(
                                key=key, axis=self.obj._get_axis_name(axis)))
                    else:

                        # we skip the warning on Categorical/Interval
                        # as this check is actually done (check for
                        # non-missing values), but a bit later in the
                        # code, so we want to avoid warning & then
                        # just raising
                        _missing_key_warning = textwrap.dedent("""
                        Passing list-likes to .loc or [] with any missing label will raise
                        KeyError in the future, you can use .reindex() as an alternative.

                        See the documentation here:
                        http://pandas.pydata.org/pandas-docs/stable/indexing.html#deprecate-loc-reindex-listlike""")  # noqa

                        if not (ax.is_categorical() or ax.is_interval()):
                            warnings.warn(_missing_key_warning,
                                          FutureWarning, stacklevel=5)

            return True

        else:

            def error():
                if isna(key):
                    raise TypeError("cannot use label indexing with a null "
                                    "key")
                raise KeyError(u"the label [{key}] is not in the [{axis}]"
                               .format(key=key,
                                       axis=self.obj._get_axis_name(axis)))

            try:
                key = self._convert_scalar_indexer(key, axis)
                if not ax.contains(key):
                    error()
            except TypeError as e:

                # python 3 type errors should be raised
                if _is_unorderable_exception(e):
                    error()
                raise
            except:
                error()

        return True
