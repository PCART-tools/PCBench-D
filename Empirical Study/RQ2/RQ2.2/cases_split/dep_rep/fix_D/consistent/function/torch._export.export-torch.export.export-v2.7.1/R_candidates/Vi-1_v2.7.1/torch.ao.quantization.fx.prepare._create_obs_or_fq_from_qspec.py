def _create_obs_or_fq_from_qspec(
    quantization_spec: Optional[QuantizationSpecBase],
    obs_or_fq_map: dict[EdgeOrNode, ObserverOrFakeQuantize],
    is_qat: bool,
):
    """Create observer or fake quantize objects based on quantization spec

    Args:
       quantization_spec: used to store parameters to create the observer or fake quantizer
       obs_or_fq_map: this is a map from edge/output to the corresponding observer/fake_quant
       instance, it may be reused for different edge/output depending on configuration
    """
    if quantization_spec is None:
        return None
    if isinstance(quantization_spec, SharedQuantizationSpec):
        edge_or_node = quantization_spec.edge_or_node
        assert edge_or_node in obs_or_fq_map, (
            "please make sure only refer to edge or node that has "
            f"observer/fake_quant inserted: '{edge_or_node}' not in\n{obs_or_fq_map.keys()}"
        )
        return obs_or_fq_map[edge_or_node]
    elif isinstance(quantization_spec, DerivedQuantizationSpec):
        # can't use asdict, so not calling get_observer_kwargs here
        kwargs = {
            "dtype": quantization_spec.dtype,
            "derive_qparams_fn": quantization_spec.derive_qparams_fn,
            "quant_min": quantization_spec.quant_min,
            "quant_max": quantization_spec.quant_max,
            "qscheme": quantization_spec.qscheme,
            "ch_axis": quantization_spec.ch_axis,
        }
        edge_or_nodes = quantization_spec.derived_from
        obs_or_fqs = [obs_or_fq_map[k] for k in edge_or_nodes]
        kwargs["obs_or_fqs"] = obs_or_fqs
        return _DerivedObserverOrFakeQuantize.with_args(**kwargs)()
    elif isinstance(quantization_spec, FixedQParamsQuantizationSpec):
        kwargs = _get_observer_kwargs(quantization_spec)
        observer_ctr = FixedQParamsObserver.with_args(**kwargs)
        if is_qat:
            return FixedQParamsFakeQuantize.with_args(observer=observer_ctr)()
        else:
            return observer_ctr()

    assert isinstance(quantization_spec, QuantizationSpec)
    observer_or_fake_quant_ctr = quantization_spec.observer_or_fake_quant_ctr
    kwargs = _get_observer_kwargs(quantization_spec)
    kwargs.pop("observer_or_fake_quant_ctr")
    # we will remove is_dynamic from QuantizationSpec because
    # it seems that dynamic range quantization
    obs_or_fq_class = observer_or_fake_quant_ctr
    if isinstance(observer_or_fake_quant_ctr, _PartialWrapper):
        obs_or_fq_class = observer_or_fake_quant_ctr.p.func  # type: ignore[union-attr, assignment]
    if "PerChannel" not in obs_or_fq_class.__name__:  # type: ignore[operator, union-attr]
        kwargs.pop("ch_axis")
    return observer_or_fake_quant_ctr.with_args(**kwargs)()
