    def to_dict(self, outtype='dict'):
        """
        Convert DataFrame to dictionary.

        Parameters
        ----------
        outtype : str {'dict', 'list', 'series', 'records'}
            Determines the type of the values of the dictionary. The
            default `dict` is a nested dictionary {column -> {index -> value}}.
            `list` returns {column -> list(values)}. `series` returns
            {column -> Series(values)}. `records` returns [{columns -> value}].
            Abbreviations are allowed.


        Returns
        -------
        result : dict like {column -> {index -> value}}
        """
        if not self.columns.is_unique:
            warnings.warn("DataFrame columns are not unique, some "
                          "columns will be omitted.", UserWarning)
        if outtype.lower().startswith('d'):
            return dict((k, v.to_dict()) for k, v in compat.iteritems(self))
        elif outtype.lower().startswith('l'):
            return dict((k, v.tolist()) for k, v in compat.iteritems(self))
        elif outtype.lower().startswith('s'):
            return dict((k, v) for k, v in compat.iteritems(self))
        elif outtype.lower().startswith('r'):
            return [dict((k, v) for k, v in zip(self.columns, row))
                    for row in self.values]
        else:  # pragma: no cover
            raise ValueError("outtype %s not understood" % outtype)
