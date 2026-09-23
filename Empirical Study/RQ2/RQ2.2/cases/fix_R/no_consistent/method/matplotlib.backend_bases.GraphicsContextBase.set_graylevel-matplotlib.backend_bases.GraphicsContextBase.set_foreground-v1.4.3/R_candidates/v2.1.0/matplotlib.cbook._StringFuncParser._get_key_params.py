    def _get_key_params(self):
        str_func = self._str_func
        # Checking if it comes with parameters
        regex = r'\{(.*?)\}'
        params = re.findall(regex, str_func)

        for i, param in enumerate(params):
            try:
                params[i] = float(param)
            except ValueError:
                raise ValueError("Parameter %i is '%s', which is "
                                 "not a number." %
                                 (i, param))

        str_func = re.sub(regex, '{p}', str_func)

        try:
            func = self._funcs[str_func]
        except (ValueError, KeyError):
            raise ValueError("'%s' is an invalid string. The only strings "
                             "recognized as functions are %s." %
                             (str_func, list(self._funcs)))

        # Checking that the parameters are valid
        if not func.check_params(params):
            raise ValueError("%s are invalid values for the parameters "
                             "in %s." %
                             (params, str_func))

        return str_func, params
