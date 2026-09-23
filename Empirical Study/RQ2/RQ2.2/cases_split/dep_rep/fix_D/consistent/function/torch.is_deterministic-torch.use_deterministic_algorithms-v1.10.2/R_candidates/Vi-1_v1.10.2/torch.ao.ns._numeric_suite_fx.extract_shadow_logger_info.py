def extract_shadow_logger_info(
    model_a_shadows_b: nn.Module,
    logger_cls: Callable,
    model_name_to_use_for_layer_names: str,
) -> NSResultsType:
    """
    Same thing as extract_logger_info, but for an `a_shadows_b` model.
    TODO(future PR): real docblock
    """
    torch._C._log_api_usage_once("quantization_api._numeric_suite_fx.extract_shadow_logger_info")
    results: NSResultsType = collections.defaultdict(dict)
    _extract_logger_info_one_model(model_a_shadows_b, results, logger_cls)
    # fill in missing fqn entries
    maybe_add_missing_fqns(results)
    # rekey on the name of model b
    results = rekey_logger_info_on_node_name_of_model(
        results, model_name_to_use_for_layer_names)
    return dict(results)
