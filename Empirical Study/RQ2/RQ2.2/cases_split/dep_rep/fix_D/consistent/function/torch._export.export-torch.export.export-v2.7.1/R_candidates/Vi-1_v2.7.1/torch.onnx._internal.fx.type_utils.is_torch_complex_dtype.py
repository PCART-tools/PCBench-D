def is_torch_complex_dtype(tensor_dtype: torch.dtype) -> bool:
    # NOTE: This is needed as TorchScriptTensor is nor supported by torch.is_complex()
    return tensor_dtype in _COMPLEX_TO_FLOAT
