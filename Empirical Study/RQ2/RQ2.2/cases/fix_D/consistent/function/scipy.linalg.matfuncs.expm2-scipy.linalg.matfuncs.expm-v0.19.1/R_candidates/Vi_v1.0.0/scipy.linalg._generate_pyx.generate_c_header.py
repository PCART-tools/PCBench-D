def generate_c_header(func_sigs, sub_sigs, all_sigs, lib_name):
    funcs = "".join(c_func_decl(*sig) for sig in func_sigs)
    subs = "\n" + "".join(c_sub_decl(*sig) for sig in sub_sigs)
    if lib_name == 'LAPACK':
        preamble = (c_preamble.format(lib=lib_name) + lapack_decls)
    else:
        preamble = c_preamble.format(lib=lib_name)
    return "".join([preamble, cpp_guard, funcs, subs, c_end])
