def check_for_mutation_ignore_cuda_graph_managed_tensor(
    aot_model: torch.fx.GraphModule, num_fixed
) -> Optional[str]:
    mutation_indices = find_input_mutations(aot_model.graph) - set(range(num_fixed))
    if not mutation_indices:
        return None

    placeholders = get_placeholder_info(aot_model.graph)
    return get_mutation_stack_trace(placeholders, mutation_indices)
