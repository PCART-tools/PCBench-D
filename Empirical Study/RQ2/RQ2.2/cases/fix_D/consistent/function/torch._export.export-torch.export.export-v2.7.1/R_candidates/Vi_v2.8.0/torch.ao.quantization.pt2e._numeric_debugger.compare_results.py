def compare_results(
    ref_results: dict[int, tuple[Optional[str], object, list[torch.Tensor]]],
    actual_results: dict[int, tuple[Optional[str], object, list[torch.Tensor]]],
) -> dict[int, NodeAccuracySummary]:
    """Given two dict mapping from `debug_handle_id` (int) to list of tensors
    return a map from `debug_handle_id` to `NodeAccuracySummary` that contains
    comparison information like SQNR, MSE etc.

    Args:
        ref_results (Dict[int, Tuple[str, object, List[torch.Tensor]]]): reference results for each debug_handle_id
        actual_results (Dict[int, Tuple[str, object, List[torch.Tensor]]]): actual results for each debug_handle_id

    Returns:
        Dict[int, NodeAccuracySummary]
    """
    comparisons = {}
    for debug_handle, (ref_name, ref_stack, ref_stats) in ref_results.items():
        if debug_handle not in actual_results:
            log.debug(
                "Cannot compare for handle %s because it wasn't found in the transformed model",
                debug_handle,
            )
            continue
        actual_name, actual_stack, actual_stats = actual_results[debug_handle]
        try:
            results = [
                QuantizationComparisonResult(actual=a, ref=b)
                for a, b in zip(actual_stats, ref_stats)
            ]
        except Exception as e:
            # Add extra information for an exception from QuantizationComparisonResult
            # if the shapes didn't match, to include the handle and the node names.
            raise ValueError(
                f"For numeric_debug_handle={debug_handle} from ref node {ref_name} and actual node {actual_name}"
            ) from e

        comparisons[debug_handle] = NodeAccuracySummary(
            handle=debug_handle,
            actual_node_name=actual_name or "",
            actual_module_stack=_module_stack_to_str(actual_stack),
            ref_node_name=ref_name or "",
            ref_module_stack=_module_stack_to_str(ref_stack),
            results=results,
        )

    return comparisons
