def _get_do_arguments(do_op):
    assert do_op.type == "Do", "Expected Do op"
    args = {}
    for arg in do_op.arg:
        if not arg.name:
            continue
        if arg.name == "net":
            assert arg.n, "Expected non empty net argument"
            args["net"] = arg.n
        elif arg.name == "reuse_workspace":
            assert arg.i, "Expected non empty reuse_workspace argument"
            args["reuse_workspace"] = bool(arg.i)
        elif arg.name == "inner_blobs":
            assert arg.strings, "Expected non empty inner_blobs argument"
            args["inner_blobs"] = arg.strings
        elif arg.name == "outer_blobs_idx":
            assert arg.ints, "Expected non empty outer_blobs_idx argument"
            args["outer_blobs_idx"] = arg.ints
    return args
