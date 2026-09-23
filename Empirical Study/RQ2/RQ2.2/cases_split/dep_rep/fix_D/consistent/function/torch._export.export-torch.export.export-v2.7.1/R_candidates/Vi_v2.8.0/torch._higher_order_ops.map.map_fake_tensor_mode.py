@map_impl.py_impl(FakeTensorMode)
def map_fake_tensor_mode(mode, f, xs, args):
    with mode:
        return map_dense(f, xs, args)
