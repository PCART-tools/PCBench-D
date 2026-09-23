    def _convert_key(self, key):
        """ require  integer args (and convert to label arguments) """
        ckey = []
        for a, i in zip(self.obj.axes, key):
            if not com.is_integer(i):
                raise ValueError("iAt based indexing can only have integer "
                                 "indexers")
            ckey.append(a[i])
        return ckey
