def create_trt_operator_support(use_implicit_batch_dim=True) -> ops.OperatorSupportBase:
    """Creates an `OperatorSupportBase` instance used for TRT splitting purpose.
    """
    # Create an `OperatorSupport` that declares a node supported if it
    # finds a registered TRT converter.
    support_dict: Dict[str, None] = {}
    for k in CONVERTERS.keys():
        if use_implicit_batch_dim:
            if k not in NO_IMPLICIT_BATCH_DIM_SUPPORT.keys():
                support_dict[get_acc_ops_name(k)] = None
        elif k not in NO_EXPLICIT_BATCH_DIM_SUPPORT.keys():
            support_dict[get_acc_ops_name(k)] = None
    supported_if_converter_registered = ops.OperatorSupport(
        support_dict=support_dict
    )

    return ops.chain(
        # 1. Node is not supported if it has args with int64 dtype:
        ops.OpSupports.decline_if_input_dtype(torch.int64),
        # 2. Node is supported if it has TRT converter:
        supported_if_converter_registered,
    )
