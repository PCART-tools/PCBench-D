def generate_fused_funcs(modname, ufunc_fn_prefix, fused_funcs):
    pwd = os.path.dirname(__file__)
    pxdfile = os.path.join(pwd, modname + ".pxd")
    pyxfile = os.path.join(pwd, modname + ".pyx")
    proto_h_filename = os.path.join(pwd, ufunc_fn_prefix + '_defs.h')

    sources = []
    declarations = []
    # Code for benchmarks
    bench_aux = []
    fused_types = set()
    # Parameters for the tests
    doc = []
    defs = []

    for func in fused_funcs:
        if func.name.startswith("_"):
            # Don't try to deal with functions that have extra layers
            # of wrappers.
            continue

        # Get the function declaration for the .pxd and the source
        # code for the .pyx
        dec, src, specs, func_fused_types, wrap = func.generate()
        declarations.append(dec)
        sources.append(src)
        if wrap:
            sources.append(wrap)
        fused_types.update(func_fused_types)

        # Declare the specializations
        cfuncs = func.get_prototypes(nptypes_for_h=True)
        for c_name, c_proto, cy_proto, header in cfuncs:
            if header.endswith('++'):
                # We grab the c++ functions from the c++ module
                continue
            item_defs, _, _ = get_declaration(func, c_name, c_proto,
                                              cy_proto, header,
                                              proto_h_filename)
            defs.extend(item_defs)

        # Add a line to the documentation
        doc.append(generate_doc(func.name, specs))

        # Generate code for benchmarks
        if func.name in CYTHON_SPECIAL_BENCHFUNCS:
            for codes in CYTHON_SPECIAL_BENCHFUNCS[func.name]:
                pybench, cybench = generate_bench(func.name, codes)
                bench_aux.extend([pybench, cybench])

    fused_types = list(fused_types)
    fused_types.sort()

    with open(pxdfile, 'w') as f:
        f.write(CYTHON_SPECIAL_PXD)
        f.write("\n")
        f.write("\n\n".join(fused_types))
        f.write("\n\n")
        f.write("\n".join(declarations))
    with open(pyxfile, 'w') as f:
        header = CYTHON_SPECIAL_PYX
        header = header.replace("FUNCLIST", "\n".join(doc))
        f.write(header)
        f.write("\n")
        f.write("\n".join(defs))
        f.write("\n\n")
        f.write("\n\n".join(sources))
        f.write("\n\n")
        f.write("\n\n".join(bench_aux))
