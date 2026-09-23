def get_ns_op_name_from_custom_op(symbolic_name):
    if not bool(re.match(r"^[a-zA-Z0-9-_]*::[a-zA-Z-_]+[a-zA-Z0-9-_]*$", symbolic_name)):
        raise ValueError("Failed to register operator {}. \
                          The symbolic name must match the format Domain::Name, \
                          and should start with a letter and contain only \
                          alphanumerical characters".format(symbolic_name))
    ns, op_name = symbolic_name.split("::")
    if ns == "onnx":
        raise ValueError("Failed to register operator {}. \
                          {} domain cannot be modified."
                         .format(symbolic_name, ns))

    if ns == "aten":
        ns = ""

    return ns, op_name
