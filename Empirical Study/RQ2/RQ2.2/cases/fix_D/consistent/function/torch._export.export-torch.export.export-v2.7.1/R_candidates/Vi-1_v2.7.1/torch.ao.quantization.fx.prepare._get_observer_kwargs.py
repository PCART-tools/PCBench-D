def _get_observer_kwargs(
    quant_spec: Union[QuantizationSpec, FixedQParamsQuantizationSpec]
):
    kwargs_dict = asdict(quant_spec)
    return copy.deepcopy(kwargs_dict)
