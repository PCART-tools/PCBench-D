    @classmethod
    def from_dict(cls, data, orient='columns', dtype=None):
        """
        Construct DataFrame from dict of array-like or dicts

        Parameters
        ----------
        data : dict
            {field : array-like} or {field : dict}
        orient : {'columns', 'index'}, default 'columns'
            The "orientation" of the data. If the keys of the passed dict
            should be the columns of the resulting DataFrame, pass 'columns'
            (default). Otherwise if the keys should be rows, pass 'index'.
        dtype : dtype, default None
            Data type to force, otherwise infer

        Returns
        -------
        DataFrame
        """
        index, columns = None, None
        orient = orient.lower()
        if orient == 'index':
            if len(data) > 0:
                # TODO speed up Series case
                if isinstance(list(data.values())[0], (Series, dict)):
                    data = _from_nested_dict(data)
                else:
                    data, index = list(data.values()), list(data.keys())
        elif orient != 'columns':  # pragma: no cover
            raise ValueError('only recognize index or columns for orient')

        return cls(data, index=index, columns=columns, dtype=dtype)
