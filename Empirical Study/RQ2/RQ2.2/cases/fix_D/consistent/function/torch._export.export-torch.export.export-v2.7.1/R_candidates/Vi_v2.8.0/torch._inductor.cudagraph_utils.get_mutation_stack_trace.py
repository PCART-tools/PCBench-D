def get_mutation_stack_trace(
    placeholders: Sequence[PlaceholderInfo], mutation_indices: Sequence[int]
) -> str:
    stack_trace: Optional[str] = ""

    for idx in mutation_indices:
        placeholder = placeholders[idx]
        if stack_trace := get_mutating_use_stack_trace(placeholder):
            break

    msg = format_default_skip_message(
        f"mutated inputs ({len(mutation_indices)} instances)"
    )
    if stack_trace:
        return f"{msg}. Found from : \n {stack_trace}"

    return msg
