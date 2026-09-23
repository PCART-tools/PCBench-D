    def hash_array(vals):
        """Given a 1d array, return an array of deterministic integers."""
        # work with cagegoricals as ints. (This check is above the complex
        # check so that we don't ask numpy if categorical is a subdtype of
        # complex, as it will choke.
        if is_categorical_dtype(vals.dtype):
            vals = vals.codes

        # we'll be working with everything as 64-bit values, so handle this
        # 128-bit value early
        if np.issubdtype(vals.dtype, np.complex128):
            return hash_array(vals.real) + 23 * hash_array(vals.imag)

        # MAIN LOGIC:

        # First, turn whatever array this is into unsigned 64-bit ints, if we can
        # manage it.
        if vals.dtype == np.bool:
            vals = vals.astype('u8')

        elif (np.issubdtype(vals.dtype, np.datetime64) or
              np.issubdtype(vals.dtype, np.timedelta64) or
              np.issubdtype(vals.dtype, np.number)) and vals.dtype.itemsize <= 8:

            vals = vals.view('u{}'.format(vals.dtype.itemsize)).astype('u8')
        else:
            vals = np.array([hash(x) for x in vals], dtype=np.uint64)

        # Then, redistribute these 64-bit ints within the space of 64-bit ints
        vals ^= vals >> 30
        vals *= np.uint64(0xbf58476d1ce4e5b9)
        vals ^= vals >> 27
        vals *= np.uint64(0x94d049bb133111eb)
        vals ^= vals >> 31
        return vals
