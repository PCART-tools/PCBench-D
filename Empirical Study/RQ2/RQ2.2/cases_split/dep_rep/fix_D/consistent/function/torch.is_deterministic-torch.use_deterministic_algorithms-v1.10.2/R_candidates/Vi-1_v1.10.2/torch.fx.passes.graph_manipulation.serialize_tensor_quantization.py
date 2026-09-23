@compatibility(is_backward_compatible=False)
def serialize_tensor_quantization(
    tensor: torch.Tensor, weights: Dict, pcq_prefix: str
) -> Tuple[Dict, Dict]:
    """
    Args:
        tensor: The tensor from which we try to extract quantization information.
        weights: A dict that contains mapping from name to a tensor value.
        pcq_prefix: A string that we would use later on as prefix for per channel quantization information. This
            usually would be the key that we use to store info of `tensor`.

    Returns:
        scheme: Dict that stores the quantization information of `tensor`.
        per_channel_dict: Dict that stores the information of per_channel_scales and
            per_channel_zero_points of `tensor`. This Will be empty if `tensor` is not
            per channel quantized.

    `tensor` is per tensor quantized:
        scheme: {
            "qscheme": str(tensor.qscheme()),
            "q_scale": tensor.q_scale(),
            "q_zero_point": tensor.q_zero_point(),
        }

    `tensor` is per channel quantized:
        scheme: {
            "qscheme": str(tensor.qscheme()),
            "q_per_channel_scales": {pcq_prefix}_per_channel_scales,
            "q_per_channel_zero_points": {pcq_prefix}_per_channel_zero_points,
            "q_per_channel_axis": tensor.q_per_channel_axis()
        }
        per_channel_dict: {
            {pcq_prefix}_per_channel_scales: {
                "dtype": dtype,
                "shape": shape,
                "is_quantized": is_quantized,
                "stride": stride,
            }
            {pcq_prefix}_per_channel_zero_points: {
                "dtype": dtype,
                "shape": shape,
                "is_quantized": is_quantized,
                "stride": stride,
            }
        }
        weights would be updated with {
            {pcq_prefix}_per_channel_scales: tensor.q_per_channel_scales().float()
            {pcq_prefix}_per_channel_zero_points: tensor.q_per_channel_zero_points().int()
        }
    """
    scheme: Dict[str, Any] = {}
    per_channel_dict: Dict[str, Dict] = {}

    if not tensor.is_quantized:
        return scheme, per_channel_dict

    scheme["qscheme"] = str(tensor.qscheme())

    # For per tensor scheme, we stores scale and zero_point.
    if tensor.qscheme() in {torch.per_tensor_affine, torch.per_tensor_symmetric}:
        scheme["q_scale"] = tensor.q_scale()
        scheme["q_zero_point"] = tensor.q_zero_point()

    # For per channel scheme, per_channel_scales and per_channel_zero_points are tensors.
    # We store their tensor value into `weights` and store the name into `scheme`.
    if tensor.qscheme() in {
        torch.per_channel_affine,
        torch.per_channel_affine_float_qparams,
        torch.per_channel_symmetric,
    }:
        # per_channel_scales is float64. Here we save it as float32.
        weights[
            f"{pcq_prefix}_per_channel_scales"
        ] = tensor.q_per_channel_scales().float()
        scheme["q_per_channel_scales"] = f"{pcq_prefix}_per_channel_scales"
        per_channel_dict.update(
            serialize_weight(
                weights[f"{pcq_prefix}_per_channel_scales"],
                weights,
                f"{pcq_prefix}_per_channel_scales",
            )
        )

        # per_channel_zero_point is int64. Here we save it as int32.
        weights[
            f"{pcq_prefix}_per_channel_zero_points"
        ] = tensor.q_per_channel_zero_points().int()
        scheme["q_per_channel_zero_points"] = f"{pcq_prefix}_per_channel_zero_points"
        per_channel_dict.update(
            serialize_weight(
                weights[f"{pcq_prefix}_per_channel_zero_points"],
                weights,
                f"{pcq_prefix}_per_channel_zero_points",
            )
        )

        scheme["q_per_channel_axis"] = tensor.q_per_channel_axis()
    return scheme, per_channel_dict
