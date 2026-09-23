def grab_specific_steps(
    steps_to_grab: List[str], job: Dict[str, Any]
) -> List[Dict[str, Any]]:
    relevant_steps = []
    for step in steps_to_grab:
        for actual_step in job["steps"]:
            if actual_step["name"].lower().strip() == step.lower().strip():
                relevant_steps.append(actual_step)
                break

    if len(relevant_steps) != len(steps_to_grab):
        raise RuntimeError(f"Missing steps:\n{relevant_steps}\n{steps_to_grab}")

    return relevant_steps
