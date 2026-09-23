def generate_fused_type(codes):
    """
    Generate name of and cython code for a fused type.

    Parameters
    ----------
    typecodes : str
        Valid inputs to CY_TYPES (i.e. f, d, g, ...).

    """
    cytypes = map(lambda x: CY_TYPES[x], codes)
    name = codes + "_number_t"
    declaration = ["ctypedef fused " + name + ":"]
    for cytype in cytypes:
        declaration.append("    " + cytype)
    declaration = "\n".join(declaration)
    return name, declaration
