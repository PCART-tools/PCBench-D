def main():
    p = optparse.OptionParser(usage=__doc__.strip())
    options, args = p.parse_args()
    if len(args) != 0:
        p.error('invalid number of arguments')

    ufuncs = Ufunc.parse_all(FUNCS)
    generate_ufuncs("_ufuncs", "_ufuncs_cxx", ufuncs)
    fused_funcs = FusedFunc.parse_all(FUNCS)
    generate_fused_funcs("cython_special", "_ufuncs", fused_funcs)
