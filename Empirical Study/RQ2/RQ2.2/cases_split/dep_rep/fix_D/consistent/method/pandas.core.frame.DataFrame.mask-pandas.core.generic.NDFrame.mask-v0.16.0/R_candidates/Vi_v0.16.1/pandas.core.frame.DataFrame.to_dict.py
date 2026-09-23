    @deprecate_kwarg(old_arg_name='outtype', new_arg_name='orient')
    def to_dict(self, orient='dict'):
        """Convert DataFrame to dictionary.

        Parameters
        ----------
        orient : str {'dict', 'list', 'series', 'split', 'records'}
            Determines the type of the values of the dictionary.

            - dict (default) : dict like {column -> {index -> value}}
            - list : dict like {column -> [values]}
            - series : dict like {column -> Series(values)}
            - split : dict like
              {index -> [index], columns -> [columns], data -> [values]}
            - records : list like
              [{column -> value}, ... , {column -> value}]

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
                    'data': self.values.tolist()}
        elif orient.lower().startswith('s'):
            return dict((k, v) for k, v in compat.iteritems(self))
        elif orient.lower().startswith('r'):
            return [dict((k, v) for k, v in zip(self.columns, row))
                    for row in self.values]
        else:
            raise ValueError("orient '%s' not understood" % orient)
