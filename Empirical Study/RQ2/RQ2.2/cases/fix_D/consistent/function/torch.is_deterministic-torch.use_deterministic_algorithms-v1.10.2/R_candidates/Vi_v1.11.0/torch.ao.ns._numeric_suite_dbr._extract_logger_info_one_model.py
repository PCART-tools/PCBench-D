def _extract_logger_info_one_model(model: torch.nn.Module) -> Tuple[str, Any]:
    results: Optional[List[List[Any]]] = None
    model_name = None
    for _, module in model.named_modules():
        if isinstance(module, AutoQuantizationState):
            if results is None:
                # initialize results to the right length
                results = [[] for i in range(len(module.op_outputs))]
            assert results is not None

            if model_name is None:
                # model_name is the same everywhere in this model, take
                # the first one
                model_name = module.logging_model_name

            for forward_idx, outputs in enumerate(module.op_outputs):
                results[forward_idx].extend(outputs)

    # sort each forward's results by global idx
    assert results is not None
    assert model_name is not None
    for result_idx, result in enumerate(results):
        result.sort(key=functools.cmp_to_key(  # type: ignore[misc]
            lambda a, b: 1 if a[0] > b[0] else -1))  # type: ignore[index]

    return model_name, results
