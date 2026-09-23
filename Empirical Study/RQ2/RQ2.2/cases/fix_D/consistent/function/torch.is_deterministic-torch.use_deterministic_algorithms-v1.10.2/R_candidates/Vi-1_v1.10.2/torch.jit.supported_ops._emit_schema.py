def _emit_schema(mod, name, schema, arg_start=0, padding=4):
    if mod is None:
        qualified_name = name
    else:
        qualified_name = "{}.{}".format(mod, name)
    schema_str = "{}({}) -> {}".format(qualified_name,
                                       _emit_args(len(qualified_name) + 1 + padding, schema.arguments[arg_start:]),
                                       _emit_rets(schema.returns))
    return schema_str
