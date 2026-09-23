    def properties(self):
        """
        return a dictionary mapping property name -> value
        """
        o = self.oorig
        getters = [name for name in dir(o)
                   if name.startswith('get_') and callable(getattr(o, name))]
        getters.sort()
        d = dict()
        for name in getters:
            func = getattr(o, name)
            if self.is_alias(func):
                continue

            try:
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    val = func()
            except:
                continue
            else:
                d[name[4:]] = val

        return d
