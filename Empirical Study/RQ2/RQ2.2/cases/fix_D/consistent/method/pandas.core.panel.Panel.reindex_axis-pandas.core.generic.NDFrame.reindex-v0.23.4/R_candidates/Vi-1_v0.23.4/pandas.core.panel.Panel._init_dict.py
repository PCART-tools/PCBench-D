    def _init_dict(self, data, axes, dtype=None):
        haxis = axes.pop(self._info_axis_number)

        # prefilter if haxis passed
        if haxis is not None:
            haxis = _ensure_index(haxis)
            data = OrderedDict((k, v)
                               for k, v in compat.iteritems(data)
                               if k in haxis)
        else:
            keys = com._dict_keys_to_ordered_list(data)
            haxis = Index(keys)

        for k, v in compat.iteritems(data):
            if isinstance(v, dict):
                data[k] = self._constructor_sliced(v)

        # extract axis for remaining axes & create the slicemap
        raxes = [self._extract_axis(self, data, axis=i) if a is None else a
                 for i, a in enumerate(axes)]
        raxes_sm = self._extract_axes_for_slice(self, raxes)

        # shallow copy
        arrays = []
        haxis_shape = [len(a) for a in raxes]
        for h in haxis:
            v = values = data.get(h)
            if v is None:
                values = np.empty(haxis_shape, dtype=dtype)
                values.fill(np.nan)
            elif isinstance(v, self._constructor_sliced):
                d = raxes_sm.copy()
                d['copy'] = False
                v = v.reindex(**d)
                if dtype is not None:
                    v = v.astype(dtype)
                values = v.values
            arrays.append(values)

        return self._init_arrays(arrays, haxis, [haxis] + raxes)
