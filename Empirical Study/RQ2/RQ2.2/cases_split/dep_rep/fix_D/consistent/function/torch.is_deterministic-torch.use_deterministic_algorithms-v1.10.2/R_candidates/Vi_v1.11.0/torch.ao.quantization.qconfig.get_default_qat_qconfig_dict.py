def get_default_qat_qconfig_dict(backend='fbgemm', version=1):
    qconfig = get_default_qat_qconfig(backend, version=version)
    return {
        "": qconfig,
        "object_type": [("reshape", default_reuse_input_qconfig)]
    }
