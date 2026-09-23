def export_opnames(m):
    r"""
        Generates new bytecode for a Script module and returns what the op list
        would be for a Script Module based off the current code base. If you
        have a LiteScriptModule and want to get the currently present
        list of ops call _export_operator_list instead.
    """
    return torch._C._export_opnames(m._c)
