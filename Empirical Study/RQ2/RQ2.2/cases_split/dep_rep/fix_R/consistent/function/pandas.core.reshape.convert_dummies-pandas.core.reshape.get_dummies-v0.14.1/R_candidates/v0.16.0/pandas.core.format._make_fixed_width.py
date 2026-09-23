def _make_fixed_width(strings, justify='right', minimum=None):
    if len(strings) == 0 or justify == 'all':
        return strings

    _strlen = _strlen_func()

    max_len = np.max([_strlen(x) for x in strings])

    if minimum is not None:
        max_len = max(minimum, max_len)

    conf_max = get_option("display.max_colwidth")
    if conf_max is not None and max_len > conf_max:
        max_len = conf_max

    if justify == 'left':
        justfunc = lambda self, x: self.ljust(x)
    else:
        justfunc = lambda self, x: self.rjust(x)

    def just(x):
        eff_len = max_len

        if conf_max is not None:
            if (conf_max > 3) & (_strlen(x) > max_len):
                x = x[:eff_len - 3] + '...'

        return justfunc(x, eff_len)

    result = [just(x) for x in strings]

    return result
