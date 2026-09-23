def nnc_jit(f):
    return aot_function(f, simple_ts_compile)
