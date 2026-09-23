def _to_reference(float_module, weight_qparams):
    """ Make a weighted float module (e.g. conv and linear )a reference module by
    attaching _weight_qparams that records the qparams for weight
    and change the name for the module so that it's recognized
    when people print the model
    """
    float_module._weight_qparams = weight_qparams
    float_module._register_state_dict_hook(_save_weight_qparams)
    float_module._register_load_state_dict_pre_hook(_load_weight_qparams, with_module=True)

    float_module_name = float_module._get_name()

    def _get_name():
        return float_module_name + "(Reference)"

    float_module._get_name = _get_name
