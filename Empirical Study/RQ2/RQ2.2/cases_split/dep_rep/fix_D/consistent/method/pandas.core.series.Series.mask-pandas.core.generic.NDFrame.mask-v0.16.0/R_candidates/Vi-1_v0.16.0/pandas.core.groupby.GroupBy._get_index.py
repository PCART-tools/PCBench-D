    def _get_index(self, name):
        """ safe get index, translate keys for datelike to underlying repr """

        def convert(key, s):
            # possibly convert to they actual key types
            # in the indices, could be a Timestamp or a np.datetime64

            if isinstance(s, (Timestamp,datetime.datetime)):
                return Timestamp(key)
            elif isinstance(s, np.datetime64):
                return Timestamp(key).asm8
            return key

        sample = next(iter(self.indices))
        if isinstance(sample, tuple):
            if not isinstance(name, tuple):
                msg = ("must supply a tuple to get_group with multiple"
                       " grouping keys")
                raise ValueError(msg)
            if not len(name) == len(sample):
                try:
                    # If the original grouper was a tuple
                    return self.indices[name]
                except KeyError:
                    # turns out it wasn't a tuple
                    msg = ("must supply a a same-length tuple to get_group"
                           " with multiple grouping keys")
                    raise ValueError(msg)

            name = tuple([ convert(n, k) for n, k in zip(name,sample) ])

        else:

            name = convert(name, sample)

        return self.indices[name]
