@typing_extensions.deprecated(DEPRECATION_WARNING)
def prepare(
    model,
    inplace=False,
    allow_list=None,
    observer_non_leaf_module_list=None,
    prepare_custom_config_dict=None,
):
    r"""Prepares a copy of the model for quantization calibration or quantization-aware training.

    Quantization configuration should be assigned preemptively
    to individual submodules in `.qconfig` attribute.

    The model will be attached with observer or fake quant modules, and qconfig
    will be propagated.

    Args:
        `model`: input model to be modified in-place
        `inplace`: carry out model transformations in-place, the original module is mutated
        `allow_list`: list of quantizable modules
        `observer_non_leaf_module_list`: list of non-leaf modules we want to add observer
        `prepare_custom_config_dict`: customization configuration dictionary for prepare function

    .. code-block:: python

       # Example of prepare_custom_config_dict:
       prepare_custom_config_dict = {
           # user will manually define the corresponding observed
           # module class which has a from_float class method that converts
           # float custom module to observed custom module
           "float_to_observed_custom_module_class": {CustomModule: ObservedCustomModule}
       }

    """
    torch._C._log_api_usage_once("quantization_api.quantize.prepare")
    if prepare_custom_config_dict is None:
        prepare_custom_config_dict = get_default_custom_config_dict()
    custom_module_class_mapping = prepare_custom_config_dict.get(
        "float_to_observed_custom_module_class", {}
    )

    if not inplace:
        model = copy.deepcopy(model)

    # TODO: remove allow_list
    qconfig_propagation_list = allow_list
    if allow_list is None:
        qconfig_propagation_list = get_default_qconfig_propagation_list()
    propagate_qconfig_(model, qconfig_dict=None)

    # sanity check common API misusage
    if not any(hasattr(m, "qconfig") and m.qconfig for m in model.modules()):
        warnings.warn(
            "None of the submodule got qconfig applied. Make sure you "
            "passed correct configuration through `qconfig_dict` or "
            "by assigning the `.qconfig` attribute directly on submodules"
        )

    _add_observer_(
        model,
        qconfig_propagation_list,
        observer_non_leaf_module_list,
        custom_module_class_mapping=custom_module_class_mapping,
    )
    return model
