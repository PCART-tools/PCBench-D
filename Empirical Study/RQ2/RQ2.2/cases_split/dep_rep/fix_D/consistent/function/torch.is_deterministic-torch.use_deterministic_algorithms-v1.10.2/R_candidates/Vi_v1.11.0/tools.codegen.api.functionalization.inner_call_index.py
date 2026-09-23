def inner_call_index(func: FunctionSchema) -> Optional[Binding]:
    # For view ops that return multiple tensors (like `split`), we generate a separate lambda for each output.
    # When we replay a view op that returns multiple tensors, we need to index into the output appropriately
    if len(func.returns) > 1 or (len(func.returns) == 1 and func.returns[0].type.is_list_like()):
        return mutated_view_idx_binding
    return None
