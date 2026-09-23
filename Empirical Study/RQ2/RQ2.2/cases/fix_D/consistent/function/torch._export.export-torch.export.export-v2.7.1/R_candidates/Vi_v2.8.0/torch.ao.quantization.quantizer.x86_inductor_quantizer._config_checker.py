def _config_checker(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(
        quantizer: "X86InductorQuantizer",
        name: Any,
        quantization_config: Optional["QuantizationConfig"],
    ) -> "X86InductorQuantizer":
        if quantizer._need_skip_config(quantization_config):
            warnings.warn(
                f"Skip the quantization config for {name}.",
            )
            return quantizer
        return method(quantizer, name, quantization_config)

    return wrapper
