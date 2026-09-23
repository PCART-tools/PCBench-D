@executorch_call_delegate.py_impl(FakeTensorMode)
# pyre-ignore
def call_delegate_fake_tensor_mode(mode, lowered_module, *args):
    with mode:
        return call_delegate_cpu(lowered_module, *args)
