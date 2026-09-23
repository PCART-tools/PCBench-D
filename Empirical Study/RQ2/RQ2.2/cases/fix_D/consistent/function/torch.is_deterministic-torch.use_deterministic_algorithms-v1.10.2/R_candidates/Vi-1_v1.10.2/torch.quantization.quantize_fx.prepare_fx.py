def prepare_fx(
        model: torch.nn.Module, qconfig_dict: Any,
        prepare_custom_config_dict: Optional[Dict[str, Any]] = None,
        equalization_qconfig_dict: Optional[Dict[str, Any]] = None,
        backend_config_dict: Optional[Dict[str, Any]] = None) -> ObservedGraphModule:
    r""" Prepare a model for post training static quantization

    Args:
      `model`: torch.nn.Module model, must be in eval mode
      `qconfig_dict`: qconfig_dict is a dictionary with the following configurations:
      qconfig_dict = {
      # optional, global config
      "": qconfig?,

      # optional, used for module and function types
      # could also be split into module_types and function_types if we prefer
      "object_type": [
        (torch.nn.Conv2d, qconfig?),
        (torch.nn.functional.add, qconfig?),
        ...,
       ],

      # optional, used for module names
      "module_name": [
        ("foo.bar", qconfig?)
        ...,
      ],

      # optional, matched in order, first match takes precedence
      "module_name_regex": [
        ("foo.*bar.*conv[0-9]+", qconfig?)
        ...,
      ],

      # optional, used for matching object type invocations in a submodule by
      # order
      # TODO(future PR): potentially support multiple indices ('0,1') and/or
      #   ranges ('0:3').
      "module_name_object_type_order": [
        # fully_qualified_name, object_type, index, qconfig
        ("foo.bar", torch.nn.functional.linear, 0, qconfig?),
      ],

      # priority (in increasing order):
      #   global, object_type, module_name_regex, module_name,
      #   module_name_object_type_order
      # qconfig == None means fusion and quantization should be skipped for anything
      # matching the rule
      }
      `prepare_custom_config_dict`: customization configuration dictionary for
      quantization tool:
      prepare_custom_config_dict = {
        # optional: specify the path for standalone modules
        # These modules are symbolically traced and quantized as one unit
        "standalone_module_name": [
           # module_name, qconfig_dict, prepare_custom_config_dict
           ("submodule.standalone",
            None,  # qconfig_dict for the prepare function called in the submodule,
                   # None means use qconfig from parent qconfig_dict
            {"input_quantized_idxs": [], "output_quantized_idxs": []})  # prepare_custom_config_dict
        ],

        "standalone_module_class": [
            # module_class, qconfig_dict, prepare_custom_config_dict
            (StandaloneModule,
             None,  # qconfig_dict for the prepare function called in the submodule,
                    # None means use qconfig from parent qconfig_dict
            {"input_quantized_idxs": [0], "output_quantized_idxs": [0]})  # prepare_custom_config_dict
        ],

        # user will manually define the corresponding observed
        # module class which has a from_float class method that converts
        # float custom module to observed custom module
        # (only needed for static quantization)
        "float_to_observed_custom_module_class": {
           "static": {
               CustomModule: ObservedCustomModule
           }
        },

        # the qualified names for the submodule that are not symbolically traceable
        "non_traceable_module_name": [
           "non_traceable_module"
        ],

        # the module classes that are not symbolically traceable
        # we'll also put dynamic/weight_only custom module here
        "non_traceable_module_class": [
           NonTraceableModule
        ],

        # Additional fuser_method mapping
        "additional_fuser_method_mapping": {
           (torch.nn.Conv2d, torch.nn.BatchNorm2d): fuse_conv_bn
        },

        # Additioanl module mapping for qat
        "additional_qat_module_mapping": {
           torch.nn.intrinsic.ConvBn2d: torch.nn.qat.ConvBn2d
        },

        # Additional fusion patterns
        "additional_fusion_pattern": {
           (torch.nn.BatchNorm2d, torch.nn.Conv2d): ConvReluFusionhandler
        },

        # Additional quantization patterns
        "additional_quant_pattern": {
           torch.nn.Conv2d: ConvReluQuantizeHandler,
           (torch.nn.ReLU, torch.nn.Conv2d): ConvReluQuantizeHandler,
        }

        # By default, inputs and outputs of the graph are assumed to be in
        # fp32. Providing `input_quantized_idxs` will set the inputs with the
        # corresponding indices to be quantized. Providing
        # `output_quantized_idxs` will set the outputs with the corresponding
        # indices to be quantized.
        "input_quantized_idxs": [0],
        "output_quantized_idxs": [0],

        # Attributes that are not used in forward function will
        # be removed when constructing GraphModule, this is a list of attributes
        # to preserve as an attribute of the GraphModule even when they are
        # not used in the code, these attributes will also persist through deepcopy
        "preserved_attributes": ["preserved_attr"],
      }
      `equalization_qconfig_dict`: equalization_qconfig_dict is a dictionary
      with a similar structure as qconfig_dict except it will contain
      configurations specific to equalization techniques such as input-weight
      equalization.
      `backend_config_dict`: a dictionary that specifies how operators are quantized
       in a backend, this includes how the operaetors are observed,
       supported fusion patterns, how quantize/dequantize ops are
       inserted, supported dtypes etc. The structure of the dictionary is still WIP
       and will change in the future, please don't use right now.


    Return:
      A GraphModule with observer (configured by qconfig_dict), ready for calibration

    Example:
    ```python
    import torch
    from torch.quantization import get_default_qconfig
    from torch.quantization import prepare_fx

    float_model.eval()
    qconfig = get_default_qconfig('fbgemm')
    def calibrate(model, data_loader):
        model.eval()
        with torch.no_grad():
            for image, target in data_loader:
                model(image)

    qconfig_dict = {"": qconfig}
    prepared_model = prepare_fx(float_model, qconfig_dict)
    # Run calibration
    calibrate(prepared_model, sample_inference_data)
    ```
    """
    torch._C._log_api_usage_once("quantization_api.quantize_fx.prepare_fx")
    assert not model.training, 'prepare_fx only works for models in ' + \
        'eval mode'
    return _prepare_fx(
        model,
        qconfig_dict,
        prepare_custom_config_dict,
        equalization_qconfig_dict,
        backend_config_dict)
