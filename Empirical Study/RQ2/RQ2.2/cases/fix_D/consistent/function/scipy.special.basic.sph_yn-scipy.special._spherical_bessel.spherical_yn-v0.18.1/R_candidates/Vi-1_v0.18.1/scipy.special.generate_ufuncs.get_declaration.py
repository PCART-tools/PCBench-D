def get_declaration(ufunc, c_name, c_proto, cy_proto, header, proto_h_filename):
    """
    Construct a Cython declaration of a function coming either from a
    pxd or a header file. Do sufficient tricks to enable compile-time
    type checking against the signature expected by the ufunc.
    """

    defs = []
    defs_h = []

    var_name = c_name.replace('[', '_').replace(']', '_').replace(' ', '_')

    if header.endswith('.pxd'):
        defs.append("from %s cimport %s as %s" % (
            header[:-4], ufunc.cython_func_name(c_name, prefix=""),
            ufunc.cython_func_name(c_name)))

        # check function signature at compile time
        proto_name = '_proto_%s_t' % var_name
        defs.append("ctypedef %s" % (cy_proto.replace('(*)', proto_name)))
        defs.append("cdef %s *%s_var = &%s" % (
            proto_name, proto_name, ufunc.cython_func_name(c_name, specialized=True)))
    else:
        # redeclare the function, so that the assumed
        # signature is checked at compile time
        new_name = "%s \"%s\"" % (ufunc.cython_func_name(c_name), c_name)
        defs.append("cdef extern from \"%s\":" % proto_h_filename)
        defs.append("    cdef %s" % (cy_proto.replace('(*)', new_name)))
        defs_h.append("#include \"%s\"" % header)
        defs_h.append("%s;" % (c_proto.replace('(*)', c_name)))

    return defs, defs_h, var_name
