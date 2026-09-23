def _param_rrefs(module_rref, recurse) -> List[rpc.RRef[Parameter]]:
    ret: List[rpc.RRef[Parameter]] = []
    for param in module_rref.local_value().parameters(recurse):
        ret.append(rpc.RRef(param))
    return ret
