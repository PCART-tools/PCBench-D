def get_custom_module_class_keys(custom_config_dict, custom_config_dict_key) -> List[Any]:
    r""" Get all the unique custom module keys in the custom config dict
    e.g.
    Input:
    custom_config_dict = {
        "float_to_observed_custom_module_class": {
           "static": {
               CustomModule1: ObservedCustomModule
           },
           "dynamic": {
               CustomModule2: DynamicObservedCustomModule
           },
           "weight_only": {
               CustomModule3: WeightOnlyObservedCustomModule
           },
        },
    }

    Output:
    # extract all the keys in "static", "dynamic" and "weight_only" dict
    [CustomModule1, CustomModule2, CustomModule3]
    """
    # using set to dedup
    float_custom_module_classes : Set[Any] = set()
    custom_module_mapping = custom_config_dict.get(custom_config_dict_key, {})
    for quant_mode in ["static", "dynamic", "weight_only"]:
        quant_mode_custom_module_config = custom_module_mapping.get(quant_mode, {})
        quant_mode_custom_module_classes = set(quant_mode_custom_module_config.keys())
        float_custom_module_classes |= quant_mode_custom_module_classes
    return list(float_custom_module_classes)
