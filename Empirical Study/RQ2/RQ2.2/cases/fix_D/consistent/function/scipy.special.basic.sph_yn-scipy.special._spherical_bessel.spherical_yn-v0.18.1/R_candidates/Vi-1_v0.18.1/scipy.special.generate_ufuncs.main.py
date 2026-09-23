def main():
    p = optparse.OptionParser(usage=__doc__.strip())
    options, args = p.parse_args()
    if len(args) != 0:
        p.error('invalid number of arguments')

    ufuncs = Ufunc.parse_all(UFUNCS)
    generate("_ufuncs.pyx", "_ufuncs_cxx", ufuncs)
