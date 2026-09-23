def align_inputs_from_check_idxs(
    model: Callable[[list[InputType]], Any],
    inputs_to_check: Sequence[int],
) -> Callable[[list[InputType]], Any]:
    if len(inputs_to_check) == 0:
        return model

    def run(new_inputs: list[InputType]) -> Any:
        copy_misaligned_inputs(new_inputs, inputs_to_check)
        return model(new_inputs)

    return run
