def generate_ufuncs(fn_prefix, cxx_fn_prefix, ufuncs):
    filename = fn_prefix + ".pyx"
    proto_h_filename = fn_prefix + '_defs.h'

    cxx_proto_h_filename = cxx_fn_prefix + '_defs.h'
    cxx_pyx_filename = cxx_fn_prefix + ".pyx"
    cxx_pxd_filename = cxx_fn_prefix + ".pxd"

    toplevel = ""

    # for _ufuncs*
    defs = []
    defs_h = []
    all_loops = {}

    # for _ufuncs_cxx*
    cxx_defs = []
    cxx_pxd_defs = [
        "cimport sf_error",
        "cdef void _set_action(sf_error.sf_error_t, sf_error.sf_action_t) nogil"
    ]
    cxx_defs_h = []

    ufuncs.sort(key=lambda u: u.name)

    for ufunc in ufuncs:
        # generate function declaration and type checking snippets
        cfuncs = ufunc.get_prototypes()
        for c_name, c_proto, cy_proto, header in cfuncs:
            if header.endswith('++'):
                header = header[:-2]

                # for the CXX module
                item_defs, item_defs_h, var_name = get_declaration(ufunc, c_name, c_proto, cy_proto,
                                                                   header, cxx_proto_h_filename)
                cxx_defs.extend(item_defs)
                cxx_defs_h.extend(item_defs_h)

                cxx_defs.append("cdef void *_export_%s = <void*>%s" % (
                    var_name, ufunc.cython_func_name(c_name, specialized=True, override=False)))
                cxx_pxd_defs.append("cdef void *_export_%s" % (var_name,))

                # let cython grab the function pointer from the c++ shared library
                ufunc.function_name_overrides[c_name] = "scipy.special._ufuncs_cxx._export_" + var_name
            else:
                # usual case
                item_defs, item_defs_h, _ = get_declaration(ufunc, c_name, c_proto, cy_proto, header,
                                                            proto_h_filename)
                defs.extend(item_defs)
                defs_h.extend(item_defs_h)

        # ufunc creation code snippet
        t = ufunc.generate(all_loops)
        toplevel += t + "\n"

    # Produce output
    toplevel = "\n".join(sorted(all_loops.values()) + defs + [toplevel])

    with open(filename, 'w') as f:
        f.write(UFUNCS_EXTRA_CODE_COMMON)
        f.write(UFUNCS_EXTRA_CODE)
        f.write("\n")
        f.write(toplevel)
        f.write(UFUNCS_EXTRA_CODE_BOTTOM)

    defs_h = unique(defs_h)
    with open(proto_h_filename, 'w') as f:
        f.write("#ifndef UFUNCS_PROTO_H\n#define UFUNCS_PROTO_H 1\n")
        f.write("\n".join(defs_h))
        f.write("\n#endif\n")

    cxx_defs_h = unique(cxx_defs_h)
    with open(cxx_proto_h_filename, 'w') as f:
        f.write("#ifndef UFUNCS_PROTO_H\n#define UFUNCS_PROTO_H 1\n")
        f.write("\n".join(cxx_defs_h))
        f.write("\n#endif\n")

    with open(cxx_pyx_filename, 'w') as f:
        f.write(UFUNCS_EXTRA_CODE_COMMON)
        f.write("\n")
        f.write("\n".join(cxx_defs))
        f.write("\n# distutils: language = c++\n")

    with open(cxx_pxd_filename, 'w') as f:
        f.write("\n".join(cxx_pxd_defs))
