def convert_fx(
        graph_module: GraphModule, is_reference: bool = False,
        convert_custom_config_dict: Dict[str, Any] = None,
        _remove_qconfig: bool = True) -> QuantizedGraphModule:
    r""" Convert a calibrated or trained model to a quantized model
    Args:
        `graph_module`: A prepared and calibrated/trained model (GraphModule)
        `is_reference`: flag for whether to produce a reference quantized model,
        which will be a common interface between pytorch quantization with
        other backends like accelerators
        `convert_custom_config_dict`: dictionary for custom configurations for convert function:
        convert_custom_config_dict = {

          # addtional object (module/operator) mappings that will overwrite the default
          # module mappingn
          "additional_object_mapping": {
             "static": {
                FloatModule: QuantizedModule,
                float_op: quantized_op
             },
             "dynamic": {
                FloatModule: DynamicallyQuantizedModule,
                float_op: dynamically_quantized_op
             },
          },

          # user will manually define the corresponding quantized
          # module class which has a from_observed class method that converts
          # observed custom module to quantized custom module
          "observed_to_quantized_custom_module_class": {
             "static": {
                 ObservedCustomModule: QuantizedCustomModule
             },
             "dynamic": {
                 ObservedCustomModule: QuantizedCustomModule
             },
             "weight_only": {
                 ObservedCustomModule: QuantizedCustomModule
             }
          },

          # Attributes that are not used in forward function will
          # be removed when constructing GraphModule, this is a list of attributes
          # to preserve as an attribute of the GraphModule even when they are
          # not used in the code
          "preserved_attributes": ["preserved_attr"],
        }
        `_remove_qconfig`: Option to remove the qconfig attributes in the model after convert.

    Return:
        A quantized model (GraphModule)

    Example:
    ```python
    # prepared_model: the model after prepare_fx/prepare_qat_fx and calibration/training
    quantized_model = convert_fx(prepared_model)
    ```
    """
    torch._C._log_api_usage_once("quantization_api.quantize_fx.convert_fx")
    return _convert_fx(graph_module, is_reference, convert_custom_config_dict, _remove_qconfig=_remove_qconfig)
