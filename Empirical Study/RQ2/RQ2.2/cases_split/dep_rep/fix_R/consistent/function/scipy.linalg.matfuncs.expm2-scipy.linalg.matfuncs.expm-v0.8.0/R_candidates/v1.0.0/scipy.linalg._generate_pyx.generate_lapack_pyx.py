def generate_lapack_pyx(func_sigs, sub_sigs, all_sigs, header_name):
    funcs = "\n".join(pyx_decl_func(*(s+(header_name,))) for s in func_sigs)
    subs = "\n" + "\n".join(pyx_decl_sub(*(s[::2]+(header_name,)))
                            for s in sub_sigs)
    preamble = make_lapack_pyx_preamble(all_sigs)
    return preamble + funcs + subs + lapack_py_wrappers
