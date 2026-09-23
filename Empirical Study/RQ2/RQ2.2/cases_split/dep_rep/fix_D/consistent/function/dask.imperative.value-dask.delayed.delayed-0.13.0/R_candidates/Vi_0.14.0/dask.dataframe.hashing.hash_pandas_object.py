    def hash_pandas_object(obj, index=True, encoding='utf8', hash_key=None,
                           categorize=True):
        if hash_key is None:
            hash_key = _default_hash_key

        def adder(h, hashed_to_add):
            h = np.multiply(h, np.uint(3), h)
            return np.add(h, hashed_to_add, h)

        if isinstance(obj, pd.Index):
            h = hash_array(obj.values, encoding, hash_key,
                           categorize).astype('uint64')
            h = pd.Series(h, index=obj, dtype='uint64')
        elif isinstance(obj, pd.Series):
            h = hash_array(obj.values, encoding, hash_key,
                           categorize).astype('uint64')
            if index:
                h = adder(h, hash_pandas_object(obj.index,
                                                index=False,
                                                encoding=encoding,
                                                hash_key=hash_key,
                                                categorize=categorize).values)
            h = pd.Series(h, index=obj.index, dtype='uint64')
        elif isinstance(obj, pd.DataFrame):
            cols = obj.iteritems()
            first_series = next(cols)[1]
            h = hash_array(first_series.values, encoding,
                           hash_key, categorize).astype('uint64')
            for _, col in cols:
                h = adder(h, hash_array(col.values, encoding, hash_key,
                                        categorize))
            if index:
                h = adder(h, hash_pandas_object(obj.index,
                                                index=False,
                                                encoding=encoding,
                                                hash_key=hash_key,
                                                categorize=categorize).values)

            h = pd.Series(h, index=obj.index, dtype='uint64')
        else:
            raise TypeError("Unexpected type for hashing %s" % type(obj))
        return h
