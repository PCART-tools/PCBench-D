def get_field_from_acc_out_ty(
    acc_out_ty_or_dict: Union[Tuple, Dict[str, Any]], field: str
):
    """
    After tracing NamedTuple inputs are converted to standard tuples, so we cannot
    access them by name directly. Use this helper instead.
    """
    if isinstance(acc_out_ty_or_dict, dict):
        acc_out_ty = acc_out_ty_or_dict["acc_out_ty"]
    else:
        acc_out_ty = acc_out_ty_or_dict
    return acc_out_ty[TensorMetadata._fields.index(field)]
