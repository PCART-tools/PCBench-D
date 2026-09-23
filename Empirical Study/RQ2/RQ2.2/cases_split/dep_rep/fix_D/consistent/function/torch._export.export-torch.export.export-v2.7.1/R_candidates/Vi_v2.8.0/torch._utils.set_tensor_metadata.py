def set_tensor_metadata(tensor, metadata):
    # See `get_tensor_metadata` above
    assert isinstance(metadata, dict)
    assert isinstance(tensor, torch.Tensor)
    torch._C._set_tensor_metadata(tensor, metadata)  # type: ignore[attr-defined]
