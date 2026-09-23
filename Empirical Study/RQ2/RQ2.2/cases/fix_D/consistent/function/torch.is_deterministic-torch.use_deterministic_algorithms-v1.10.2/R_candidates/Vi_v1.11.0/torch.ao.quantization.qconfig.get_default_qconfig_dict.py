def get_default_qconfig_dict(backend='fbgemm', version=0):
    qconfig = get_default_qconfig(backend)
    return {
        "": qconfig,
        "object_type": [("reshape", default_reuse_input_qconfig)]
    }
