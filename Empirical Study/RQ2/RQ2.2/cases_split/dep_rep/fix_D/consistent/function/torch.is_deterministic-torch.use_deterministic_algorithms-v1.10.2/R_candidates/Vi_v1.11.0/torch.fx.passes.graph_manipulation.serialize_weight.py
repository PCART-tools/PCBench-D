@compatibility(is_backward_compatible=False)
def serialize_weight(tensor: torch.Tensor, weights: Dict, name: str) -> Dict:
    weight_dict: Dict[str, Dict] = {name: {}}
    weight_dict[name]["dtype"] = str(tensor.dtype)
    weight_dict[name]["shape"] = serialize_shape(tensor.shape)
    weight_dict[name]["requires_grad"] = str(tensor.requires_grad)
    weight_dict[name]["is_quantized"] = tensor.is_quantized
    weight_dict[name]["stride"] = serialize_stride(tensor.stride())

    if tensor.is_quantized:
        quantization_info, per_channel_dict = serialize_tensor_quantization(
            tensor, weights, name
        )
        weight_dict[name].update(quantization_info)
        weight_dict.update(per_channel_dict)

    return weight_dict
