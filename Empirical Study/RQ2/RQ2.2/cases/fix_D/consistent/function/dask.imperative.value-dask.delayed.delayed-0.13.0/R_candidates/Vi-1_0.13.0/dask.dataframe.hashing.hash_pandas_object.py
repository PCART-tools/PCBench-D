    def hash_pandas_object(obj, index=False):
        assert index is False
        if isinstance(obj, (pd.Series, pd.Index)):
            h = hash_array(obj.values).astype('uint64')
        elif isinstance(obj, pd.DataFrame):
            cols = obj.iteritems()
            first_series = next(cols)[1]
            h = hash_array(first_series.values).astype('uint64')
            for _, col in cols:
                h = np.multiply(h, np.uint(3), h)
                h = np.add(h, hash_array(col.values), h)
        else:
            raise TypeError("Unexpected type %s" % type(obj))
        return h
