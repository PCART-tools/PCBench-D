    @classmethod
    def from_dict(cls, data, intersect=False, orient='items', dtype=None):
        """
        Construct Panel from dict of DataFrame objects

        Parameters
        ----------
        data : dict
            {field : DataFrame}
        intersect : boolean
            Intersect indexes of input DataFrames
        orient : {'items', 'minor'}, default 'items'
            The "orientation" of the data. If the keys of the passed dict
            should be the items of the result panel, pass 'items'
            (default). Otherwise if the columns of the values of the passed
            DataFrame objects should be the items (which in the case of
            mixed-dtype data you should do), instead pass 'minor'
        dtype : dtype, default None
            Data type to force, otherwise infer

        Returns
        -------
        Panel
        """
        from collections import defaultdict

        orient = orient.lower()
        if orient == 'minor':
            new_data = defaultdict(OrderedDict)
            for col, df in compat.iteritems(data):
                for item, s in compat.iteritems(df):
                    new_data[item][col] = s
            data = new_data
        elif orient != 'items':  # pragma: no cover
            raise ValueError('Orientation must be one of {items, minor}.')

        d = cls._homogenize_dict(cls, data, intersect=intersect, dtype=dtype)
        ks = list(d['data'].keys())
        if not isinstance(d['data'], OrderedDict):
            ks = list(sorted(ks))
        d[cls._info_axis_name] = Index(ks)
        return cls(**d)
