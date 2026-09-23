@torch.library.register_fake("testlib::mutating_custom_op")
def foo_impl_abstract(x, z):
    return x, z, x + z
