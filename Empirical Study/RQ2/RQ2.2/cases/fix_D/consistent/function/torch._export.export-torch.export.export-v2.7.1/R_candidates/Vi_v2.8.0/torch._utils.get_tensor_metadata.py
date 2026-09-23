def get_tensor_metadata(tensor):
    # Tensor's Metadata for serializing.
    # Currently, this only returns a dict[string, bool] specifing whether
    # `conj` or `neg` bit is set.
    assert isinstance(tensor, torch.Tensor)
    return torch._C._get_tensor_metadata(tensor)  # type: ignore[attr-defined]
