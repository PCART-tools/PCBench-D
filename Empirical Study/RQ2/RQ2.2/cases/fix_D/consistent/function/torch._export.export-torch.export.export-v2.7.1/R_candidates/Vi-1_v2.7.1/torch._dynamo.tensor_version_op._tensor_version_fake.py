@_tensor_version.py_impl(FakeTensorMode)
def _tensor_version_fake(fake_mode, self_tensor):
    """
    The initial dynamo capture of _tensor_version + _unsafe_set_version_counter turns the
    `._version` into an unbacked SymInt so that we don't need to specialize on the `._version`
    of input tensors to the graph.
    """
    return fake_mode.shape_env.create_unbacked_symint()
