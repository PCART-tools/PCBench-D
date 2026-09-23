def extract_logger_info(
    model_a: torch.nn.Module,
    model_b: torch.nn.Module,
    model_name_to_use_for_layer_names: str,
) -> Any:
    """
    Extracts intermediate activations from model_a and model_b.
    """

    model_name_a, results_a = _extract_logger_info_one_model(model_a)
    model_name_b, results_b = _extract_logger_info_one_model(model_b)
    assert len(results_a) == len(results_b), 'results length mismatch'
    results: Dict[str, Any] = {}
    if len(results_a) == 0:
        return results

    for op_idx in range(len(results_a[0])):
        # currently using global_idx for layer_name
        layer_name = (
            results_a[0][op_idx][0]
            if model_name_to_use_for_layer_names == model_name_a
            else results_a[0][op_idx][0])

        values_a = [results_a[forward_idx][op_idx][3]
                    for forward_idx in range(len(results_a))]
        values_b = [results_b[forward_idx][op_idx][3]
                    for forward_idx in range(len(results_b))]
        node_output = {
            model_name_a: [{
                'type': 'node_output',
                'values': values_a,
                'ref_node_target_type': str(results_a[0][op_idx][2]),
                'fqn': str(results_a[0][op_idx][1]),
                'index_of_arg': 0,
                'index_within_arg': 0,
            }],
            model_name_b: [{
                'type': 'node_output',
                'values': values_b,
                'ref_node_target_type': str(results_b[0][op_idx][2]),
                'fqn': str(results_b[0][op_idx][1]),
                'index_of_arg': 0,
                'index_within_arg': 0,
            }],
        }

        results[layer_name] = {
            'node_output': node_output,
        }

    return results
