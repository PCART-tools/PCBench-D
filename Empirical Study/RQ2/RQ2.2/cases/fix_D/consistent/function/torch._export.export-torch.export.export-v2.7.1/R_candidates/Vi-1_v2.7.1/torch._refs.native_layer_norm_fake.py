@torch._subclasses.fake_impls.register_op_impl(aten.native_layer_norm.default)
def native_layer_norm_fake(fake_mode, func, *args, **kwargs):
    return native_layer_norm(*args)
