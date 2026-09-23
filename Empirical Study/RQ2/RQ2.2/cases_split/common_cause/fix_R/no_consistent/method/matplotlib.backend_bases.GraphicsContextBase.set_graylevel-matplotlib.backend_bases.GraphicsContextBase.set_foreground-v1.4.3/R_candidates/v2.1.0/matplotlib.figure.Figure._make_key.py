    def _make_key(self, *args, **kwargs):
        'make a hashable key out of args and kwargs'

        def fixitems(items):
            #items may have arrays and lists in them, so convert them
            # to tuples for the key
            ret = []
            for k, v in items:
                # some objects can define __getitem__ without being
                # iterable and in those cases the conversion to tuples
                # will fail. So instead of using the iterable(v) function
                # we simply try and convert to a tuple, and proceed if not.
                try:
                    v = tuple(v)
                except Exception:
                    pass
                ret.append((k, v))
            return tuple(ret)

        def fixlist(args):
            ret = []
            for a in args:
                if iterable(a):
                    a = tuple(a)
                ret.append(a)
            return tuple(ret)

        key = fixlist(args), fixitems(six.iteritems(kwargs))
        return key
