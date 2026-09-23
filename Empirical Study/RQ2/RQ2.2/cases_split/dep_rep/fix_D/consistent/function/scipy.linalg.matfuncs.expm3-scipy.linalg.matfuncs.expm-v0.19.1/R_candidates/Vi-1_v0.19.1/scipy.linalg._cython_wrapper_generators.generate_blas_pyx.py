def generate_blas_pyx(func_sigs, sub_sigs, all_sigs, header_name):
    funcs = "\n".join(pyx_decl_func(*(s+(header_name,))) for s in func_sigs)
    subs = "\n" + "\n".join(pyx_decl_sub(*(s[::2]+(header_name,)))
                            for s in sub_sigs)
    return make_blas_pyx_preamble(all_sigs) + funcs + subs + blas_py_wrappers
