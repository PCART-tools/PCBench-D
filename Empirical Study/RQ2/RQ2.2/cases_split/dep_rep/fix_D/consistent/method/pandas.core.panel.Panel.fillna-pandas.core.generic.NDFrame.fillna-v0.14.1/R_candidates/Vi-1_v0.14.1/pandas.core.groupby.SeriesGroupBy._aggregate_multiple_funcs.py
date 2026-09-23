    def _aggregate_multiple_funcs(self, arg):
        if isinstance(arg, dict):
            columns = list(arg.keys())
            arg = list(arg.items())
        elif any(isinstance(x, (tuple, list)) for x in arg):
            arg = [(x, x) if not isinstance(x, (tuple, list)) else x
                   for x in arg]

            # indicated column order
            columns = lzip(*arg)[0]
        else:
            # list of functions / function names
            columns = []
            for f in arg:
                if isinstance(f, compat.string_types):
                    columns.append(f)
                else:
                    columns.append(f.__name__)
            arg = lzip(columns, arg)

        results = {}

        for name, func in arg:
            if name in results:
                raise SpecificationError('Function names must be unique, '
                                         'found multiple named %s' % name)

            results[name] = self.aggregate(func)

        return DataFrame(results, columns=columns)
