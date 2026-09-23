@register_meta(aten.replication_pad1d_backward)
@out_wrapper("grad_input")
def meta_replication_pad1d_backward(grad_output, input, padding):
    return _pad1d_backward_common(grad_output, input, padding, is_reflection=False)
