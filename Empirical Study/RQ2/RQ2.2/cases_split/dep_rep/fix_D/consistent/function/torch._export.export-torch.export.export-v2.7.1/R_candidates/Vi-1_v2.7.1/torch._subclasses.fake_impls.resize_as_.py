@register_op_impl(aten.resize_as_.default)
def resize_as_(fake_mode, func, *args, **kwargs):
    with in_kernel_invocation_manager(fake_mode):
        return func(*args, **kwargs)
