@contextlib.contextmanager
def set_default_tensor_type(tensor_type):
    saved_tensor_type = torch.tensor([]).type()
    torch.set_default_tensor_type(tensor_type)
    try:
        yield
    finally:
        torch.set_default_tensor_type(saved_tensor_type)
