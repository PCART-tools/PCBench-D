    def to_dict(self, orient='dict'):
        """Convert DataFrame to dictionary.

        Parameters
        ----------
        orient : str {'dict', 'list', 'series', 'split', 'records', 'index'}
            Determines the type of the values of the dictionary.

            - dict (default) : dict like {column -> {index -> value}}
            - list : dict like {column -> [values]}
            - series : dict like {column -> Series(values)}
            - split : dict like
              {index -> [index], columns -> [columns], data -> [values]}
            - records : list like
              [{column -> value}, ... , {column -> value}]
            - index : dict like {index -> {column -> value}}

              .. versionadded:: 0.17.0

            Abbreviations are allowed. `s` indicates `series` and `sp`
            indicates `split`.

        Returns
        -------
        result : dict like {column -> {index -> value}}
        """
        if not self.columns.is_unique:
            warnings.warn("DataFrame columns are not unique, some "
                          "columns will be omitted.", UserWarning)
        if orient.lower().startswith('d'):
            return dict((k, v.to_dict()) for k, v in compat.iteritems(self))
        elif orient.lower().startswith('l'):
            return dict((k, v.tolist()) for k, v in compat.iteritems(self))
        elif orient.lower().startswith('sp'):
            return {'index': self.index.tolist(),
                    'columns': self.columns.tolist(),
                    'data': lib.map_infer(self.values.ravel(),
                                          _maybe_box_datetimelike)
                    .reshape(self.values.shape).tolist()}
        elif orient.lower().startswith('s'):
            return dict((k, _maybe_box_datetimelike(v))
                        for k, v in compat.iteritems(self))
        elif orient.lower().startswith('r'):
            return [dict((k, _maybe_box_datetimelike(v))
                         for k, v in zip(self.columns, row))
                    for row in self.values]
        elif orient.lower().startswith('i'):
            return dict((k, v.to_dict()) for k, v in self.iterrows())
        else:
            raise ValueError("orient '%s' not understood" % orient)
