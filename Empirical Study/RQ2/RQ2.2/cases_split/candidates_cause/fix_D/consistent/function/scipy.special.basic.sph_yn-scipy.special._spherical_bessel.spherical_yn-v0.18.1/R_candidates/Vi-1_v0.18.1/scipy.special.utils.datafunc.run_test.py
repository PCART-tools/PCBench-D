def run_test(filename, funcs, args=[0]):
    nargs = len(args)
    if len(funcs) > 1 and nargs > 1:
        raise ValueError("nargs > 1 and len(funcs) > 1 not supported")

    data = parse_txt_data(filename)
    if data.shape[1] != len(funcs) + nargs:
        raise ValueError("data has %d items / row, but len(funcs) = %d and "
                         "nargs = %d" % (data.shape[1], len(funcs), nargs))

    if nargs > 1:
        f = funcs[0]
        x = [data[args[i]] for i in nargs]
        return f(*x)
    else:
        y = []
        i = 1
        for f in funcs:
            y.append(f(data[:, 0]) - data[:, i])
            i += 1

        return data[:, 0], y
