def generate_bench(name, codes):
    tab = " "*4
    top, middle, end = [], [], []

    tmp = codes.split("*")
    if len(tmp) > 1:
        incodes = tmp[0]
        outcodes = tmp[1]
    else:
        incodes = tmp[0]
        outcodes = ""

    inargs, inargs_and_types = [], []
    for n, code in enumerate(incodes):
        arg = "x{}".format(n)
        inargs.append(arg)
        inargs_and_types.append("{} {}".format(CY_TYPES[code], arg))
    line = "def {{}}(int N, {}):".format(", ".join(inargs_and_types))
    top.append(line)
    top.append(tab + "cdef int n")

    outargs = []
    for n, code in enumerate(outcodes):
        arg = "y{}".format(n)
        outargs.append("&{}".format(arg))
        line = "cdef {} {}".format(CY_TYPES[code], arg)
        middle.append(tab + line)

    end.append(tab + "for n in range(N):")
    end.append(2*tab + "{}({})")
    pyfunc = "_bench_{}_{}_{}".format(name, incodes, "py")
    cyfunc = "_bench_{}_{}_{}".format(name, incodes, "cy")
    pytemplate = "\n".join(top + end)
    cytemplate = "\n".join(top + middle + end)
    pybench = pytemplate.format(pyfunc, "_ufuncs." + name, ", ".join(inargs))
    cybench = cytemplate.format(cyfunc, name, ", ".join(inargs + outargs))
    return pybench, cybench
