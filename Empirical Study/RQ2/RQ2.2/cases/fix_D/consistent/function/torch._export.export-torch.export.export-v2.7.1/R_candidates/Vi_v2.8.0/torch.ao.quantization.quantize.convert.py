@typing_extensions.deprecated(DEPRECATION_WARNING)
def convert(
    module,
    mapping=None,
    inplace=False,
    remove_qconfig=True,
    is_reference=False,
    convert_custom_config_dict=None,
    use_precomputed_fake_quant=False,
):
    r"""Converts submodules in input module to a different module according to `mapping`
    by calling `from_float` method on the target module class. And remove qconfig at the
    end if remove_qconfig is set to True.

    Args:
        `module`: prepared and calibrated module
        `mapping`: a dictionary that maps from source module type to target
                   module type, can be overwritten to allow swapping user defined
                   Modules
        `inplace`: carry out model transformations in-place, the original module
                   is mutated
        `convert_custom_config_dict`: custom configuration dictionary for convert function
        `use_precomputed_fake_quant`: a flag to enable use of precomputed fake quant

    .. code-block:: python

       # Example of convert_custom_config_dict:
       convert_custom_config_dict = {
           # user will manually define the corresponding quantized
           # module class which has a from_observed class method that converts
           # observed custom module to quantized custom module
           "observed_to_quantized_custom_module_class": {
               ObservedCustomModule: QuantizedCustomModule
           }
       }

    """
    torch._C._log_api_usage_once("quantization_api.quantize.convert")
    if not inplace:
        module = copy.deepcopy(module)
    _convert(
        module,
        mapping,
        inplace=True,
        is_reference=is_reference,
        convert_custom_config_dict=convert_custom_config_dict,
        use_precomputed_fake_quant=use_precomputed_fake_quant,
    )
    if remove_qconfig:
        _remove_qconfig(module)
    return module
