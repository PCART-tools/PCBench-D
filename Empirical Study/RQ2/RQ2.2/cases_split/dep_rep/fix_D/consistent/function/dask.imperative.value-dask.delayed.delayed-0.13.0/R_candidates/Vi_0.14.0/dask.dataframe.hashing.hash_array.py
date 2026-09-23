    def hash_array(vals, encoding='utf8', hash_key=None, categorize=True):
        if hash_key is None:
            hash_key = _default_hash_key

        # For categoricals, we hash the categories, then remap the codes to the
        # hash values. (This check is above the complex check so that we don't
        # ask numpy if categorical is a subdtype of complex, as it will choke.
        if is_categorical_dtype(vals.dtype):
            return _hash_categorical(vals, encoding, hash_key)

        # we'll be working with everything as 64-bit values, so handle this
        # 128-bit value early
        if np.issubdtype(vals.dtype, np.complex128):
            return hash_array(vals.real) + 23 * hash_array(vals.imag)

        # First, turn whatever array this is into unsigned 64-bit ints, if we
        # can manage it.
        if is_bool_array(vals):
            vals = vals.astype('u8')
        elif ((is_datetime64_dtype(vals) or
               is_timedelta64_dtype(vals) or
               is_numeric_dtype(vals)) and vals.dtype.itemsize <= 8):
            vals = vals.view('u{}'.format(vals.dtype.itemsize)).astype('u8')
        else:
            # With repeated values, its MUCH faster to categorize object
            # dtypes, then hash and rename categories. We allow skipping the
            # categorization when the values are known/likely to be unique.
            if categorize:
                codes, categories = pd.factorize(vals, sort=False)
                cat = pd.Categorical(codes, pd.Index(categories),
                                     ordered=False, fastpath=True)
                return _hash_categorical(cat, encoding, hash_key)

            vals = hash_object_array(vals, hash_key, encoding)

        # Then, redistribute these 64-bit ints within the space of 64-bit ints
        vals ^= vals >> 30
        vals *= np.uint64(0xbf58476d1ce4e5b9)
        vals ^= vals >> 27
        vals *= np.uint64(0x94d049bb133111eb)
        vals ^= vals >> 31
        return vals
