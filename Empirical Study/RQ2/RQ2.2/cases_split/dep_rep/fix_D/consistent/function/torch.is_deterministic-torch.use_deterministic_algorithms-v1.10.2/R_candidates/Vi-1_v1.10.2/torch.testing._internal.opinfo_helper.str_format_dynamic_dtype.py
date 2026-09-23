def str_format_dynamic_dtype(op):
    fmt_str = """
        OpInfo({name},
               dtypes={dtypesIfCPU},
               dtypesIfCUDA={dtypesIfCUDA},
        )
        """.format(name=op.name,
                   dtypesIfCPU=dtypes_dispatch_hint(op.dtypesIfCPU).dispatch_fn_str,
                   dtypesIfCUDA=dtypes_dispatch_hint(op.dtypesIfCUDA).dispatch_fn_str)

    return fmt_str
