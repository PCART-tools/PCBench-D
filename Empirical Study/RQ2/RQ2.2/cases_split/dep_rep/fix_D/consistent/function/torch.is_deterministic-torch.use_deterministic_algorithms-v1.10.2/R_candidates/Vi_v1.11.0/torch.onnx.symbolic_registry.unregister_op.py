def unregister_op(opname, domain, version):
    global _registry
    if is_registered_op(opname, domain, version):
        del _registry[(domain, version)][opname]
        if not _registry[(domain, version)]:
            del _registry[(domain, version)]
    else:
        warnings.warn("The opname " + opname + " is not registered.")
