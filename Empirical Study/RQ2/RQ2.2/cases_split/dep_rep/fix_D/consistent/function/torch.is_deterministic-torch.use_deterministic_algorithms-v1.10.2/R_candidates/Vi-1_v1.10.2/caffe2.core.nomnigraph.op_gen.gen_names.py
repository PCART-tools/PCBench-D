def gen_names(op_list):
    f = ""
    for op in op_list:
        f += dedent(
            """
            case NNKind::{name}:
                return \"{name}\";
            """.format(
                name=op
            )
        )
    return f
