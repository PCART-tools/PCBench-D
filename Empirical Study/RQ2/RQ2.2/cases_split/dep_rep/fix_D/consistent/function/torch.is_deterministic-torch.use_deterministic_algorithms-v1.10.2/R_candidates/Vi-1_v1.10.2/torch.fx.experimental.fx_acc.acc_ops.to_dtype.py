@register_acc_op
def to_dtype(input, acc_out_ty=None):
    assert acc_out_ty is not None, "valid acc_out_ty needed"
    return input.to(dtype=acc_utils.get_field_from_acc_out_ty(acc_out_ty, "dtype"))
