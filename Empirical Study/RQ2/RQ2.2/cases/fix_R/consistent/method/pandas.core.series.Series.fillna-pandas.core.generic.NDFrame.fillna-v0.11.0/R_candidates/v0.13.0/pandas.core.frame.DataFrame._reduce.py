    def _reduce(self, op, axis=0, skipna=True, numeric_only=None,
                filter_type=None, **kwds):
        axis = self._get_axis_number(axis)
        f = lambda x: op(x, axis=axis, skipna=skipna, **kwds)
        labels = self._get_agg_axis(axis)

        # exclude timedelta/datetime unless we are uniform types
        if axis == 1 and self._is_mixed_type and len(set(self.dtypes) &
                                                     _DATELIKE_DTYPES):
            numeric_only = True

        if numeric_only is None:
            try:
                values = self.values
                result = f(values)
            except Exception as e:

                # try by-column first
                if filter_type is None and axis == 0:
                    try:
                        return self.apply(f).iloc[0]
                    except:
                        pass

                if filter_type is None or filter_type == 'numeric':
                    data = self._get_numeric_data()
                elif filter_type == 'bool':
                    data = self._get_bool_data()
                else:  # pragma: no cover
                    e = NotImplementedError("Handling exception with filter_"
                                            "type %s not implemented."
                                            % filter_type)
                    raise_with_traceback(e)
                result = f(data.values)
                labels = data._get_agg_axis(axis)
        else:
            if numeric_only:
                if filter_type is None or filter_type == 'numeric':
                    data = self._get_numeric_data()
                elif filter_type == 'bool':
                    data = self._get_bool_data()
                else:  # pragma: no cover
                    msg = ("Generating numeric_only data with filter_type %s"
                           "not supported." % filter_type)
                    raise NotImplementedError(msg)
                values = data.values
                labels = data._get_agg_axis(axis)
            else:
                values = self.values
            result = f(values)

        if result.dtype == np.object_:
            try:
                if filter_type is None or filter_type == 'numeric':
                    result = result.astype(np.float64)
                elif filter_type == 'bool' and notnull(result).all():
                    result = result.astype(np.bool_)
            except (ValueError, TypeError):

                # try to coerce to the original dtypes item by item if we can
                if axis == 0:
                    result = com._coerce_to_dtypes(result, self.dtypes)

        return Series(result, index=labels)
