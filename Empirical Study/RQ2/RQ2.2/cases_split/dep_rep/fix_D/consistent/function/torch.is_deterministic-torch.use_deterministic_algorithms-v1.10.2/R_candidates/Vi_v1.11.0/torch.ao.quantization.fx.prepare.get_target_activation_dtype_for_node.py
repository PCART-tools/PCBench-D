def get_target_activation_dtype_for_node(
    node: Node,
    qconfig: QConfigAny,
    inputs_seen_counter: int,
    outputs_seen_counter: int,
    input_quantized_idxs: List[int],
    output_quantized_idxs: List[int],
    qhandler: Optional[QuantizeHandler],
    modules: Dict[str, torch.nn.Module],
    cache_for_no_tensor_check: Dict[Node, bool],
) -> Dict[str, Optional[torch.dtype]]:
    """
    Returns the expected dtype of the input and output of this node after
    convert. If the value is not None, it represents the dtype of the
    Tensor. If the value is None, it means the value is not a Tensor.

    Note: this is for activations only, weight dtypes are not handled here.

    TODO(future PR, if needed): explicitly spell out the non-Tensor
    dtypes.
    """
    if node.op == 'placeholder':
        if inputs_seen_counter in input_quantized_idxs:
            return {
                "input_activation_dtype": torch.quint8,
                "output_activation_dtype": torch.quint8,
            }
        else:
            # if dtype is fp32 (default), do nothing
            # note: other dtypes are not supported
            return {
                "input_activation_dtype": torch.float,
                "output_activation_dtype": torch.float,
            }

    elif node.op in ('call_module', 'call_method', 'call_function'):
        args_have_no_tensors = \
            all_node_args_have_no_tensors(
                node, modules, cache_for_no_tensor_check)
        if args_have_no_tensors:
            return {
                "input_activation_dtype": None,
                "output_activation_dtype": None,
            }

        # TODO(future PR): consider stopping matching getitem
        is_getitem = node.op == 'call_function' and \
            node.target == operator.getitem
        if is_getitem:
            return {
                "input_activation_dtype": torch.float,
                "output_activation_dtype": torch.float,
            }

        # get qconfig to determine the eventual dtype of this node
        if qconfig is not None:
            if qhandler is not None and qhandler.input_output_observed() and qhandler.is_output_quantized(qconfig):
                act_dtype, weight_dtype, act_compute_dtype = \
                    get_qconfig_dtypes(qconfig)
                bias_dtype = torch.float16 \
                    if act_dtype == torch.float16 and weight_dtype == torch.float16 \
                    else torch.float
                return {
                    "input_activation_dtype": act_dtype,
                    "weight_dtype": weight_dtype,
                    "bias_dtype": bias_dtype,
                    "output_activation_dtype": act_dtype,
                }
        return {
            "input_activation_dtype": torch.float,
            "output_activation_dtype": torch.float,
        }

    elif node.op == 'get_attr':
        return {
            "input_activation_dtype": torch.float,
            "output_activation_dtype": torch.float,
        }

    elif node.op == 'output':
        if outputs_seen_counter in output_quantized_idxs:
            return {
                "input_activation_dtype": torch.quint8,
                "output_activation_dtype": torch.quint8
            }
        else:
            # if dtype is fp32 (default), do nothing
            # note: other dtypes are not supported
            return {
                "input_activation_dtype": torch.float,
                "output_activation_dtype": torch.float,
            }

    else:
        raise AssertionError(f'need to handle {node.format_node()}')
