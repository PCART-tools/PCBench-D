def _convert_safetensors_to_torch_format(safetensors_file):
    # It this function is called, safetensors is guaranteed to exist
    # because the HF model with safetensors was already loaded and exported to ONNX
    from safetensors import safe_open  # type: ignore[import-not-found, import-untyped]

    tensors = {}
    with safe_open(safetensors_file, framework="pt", device="cpu") as f:  # type: ignore[attr-defined]
        for k in f.keys():
            tensors[k] = f.get_tensor(k).cpu()
    return tensors
