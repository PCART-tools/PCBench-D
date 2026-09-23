    @staticmethod
    def convert(value, unit, axis):
        """Uses axis.unit_data map to encode
        data as floats
        """
        vmap = dict(zip(axis.unit_data.seq, axis.unit_data.locs))

        if isinstance(value, six.string_types):
            return vmap[value]

        vals = shim_array(value)

        for lab, loc in vmap.items():
            vals[vals == lab] = loc

        return vals.astype('float')
