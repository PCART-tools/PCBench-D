def build_ignore_context_manager(ctx, stmt):
    InputType = namedtuple('InputType', ['name', 'ann'])
    OutputType = namedtuple('OutputType', ['name', 'ann'])

    def process_ins_outs(args):
        # parse the context manager to figure out inputs and outputs
        # with their annotated types
        # TODO: add input, output validator
        inputs = []
        outputs = []
        for arg in args:
            var_name = arg.arg
            if sys.version_info < (3, 8):
                # Starting python3.8 ast.Str is deprecated
                var_ann = arg.value.s
            else:
                var_ann = arg.value.value
            var_decl_type, var_ann = var_ann.split(":")
            if var_decl_type == "inp":
                inputs.append(InputType(var_name, var_ann))
            if var_decl_type == "out":
                outputs.append(OutputType(var_name, var_ann))
        return inputs, outputs

    def create_unique_name_ext(ctx, stmt):
        # extension will be based on the full path filename plus
        # the line number of original context manager
        return ctx.filename.replace(".", "_").replace("/", "_") + "_" + str(stmt.lineno)

    def build_return_ann_stmt(outputs):
        return_type_ann = ""
        return_statement_str = "return "
        if len(outputs) == 0:
            return_type_ann += " -> None"
        if len(outputs) == 1:
            return_type_ann = " -> " + outputs[0].ann
            return_statement_str += outputs[0].name
        if len(outputs) > 1:
            return_type_ann = " -> Tuple"
            return_type_ann += "[" + ", ".join([var.ann for var in outputs]) + "]"
            return_statement_str += ", ".join([var.name for var in outputs])
        return return_type_ann, return_statement_str

    def build_args(args):
        return ", ".join([arg.name for arg in args])

    inputs, outputs = process_ins_outs(stmt.items[0].context_expr.keywords)

    # build the replacement function str with given inputs and outputs
    ignore_function_name = "func_ignore_" + create_unique_name_ext(ctx, stmt)
    ignore_function_str = "\ndef " + ignore_function_name
    ignore_function_str += "(" + ", ".join([var.name + " :" + var.ann for var in inputs]) + ")"

    return_ann, return_stmt = build_return_ann_stmt(outputs)
    ignore_function_str += return_ann + ": pass"

    # first create the functionDef object from just declaration
    ignore_function = ast.parse(ignore_function_str).body[0]

    # dump the body of context manager to dummy function
    ignore_function.body = stmt.body  # type: ignore[attr-defined]

    # insert return statement to the function
    return_stmt = ast.parse(return_stmt).body[0]
    ignore_function.body.append(return_stmt)  # type: ignore[attr-defined]

    # registers the custom function in the global context
    ignore_func_str = "@torch.jit.ignore\n" + astunparse.unparse(ignore_function)
    ignore_func_str += "\nglobals()[\"{}\"] = {}".format(ignore_function_name, ignore_function_name)
    exec(ignore_func_str)  # noqa: P204

    # build the statements as:
    # <out_1>, <out_2>, ... = torch.jit.frontend.<func>(<in_1>, <in_2>)
    assign_str_lhs = build_args(outputs)
    # this function will be registered in torch.jit.frontend module by default
    assign_str_rhs = "torch.jit.frontend.{}(".format(ignore_function_name) + build_args(inputs) + ")"

    if len(outputs) > 0:
        assign_str = assign_str_lhs + " = " + assign_str_rhs
    else:
        assign_str = assign_str_rhs
    assign_ast = ast.parse(assign_str).body[0]
    return assign_ast
