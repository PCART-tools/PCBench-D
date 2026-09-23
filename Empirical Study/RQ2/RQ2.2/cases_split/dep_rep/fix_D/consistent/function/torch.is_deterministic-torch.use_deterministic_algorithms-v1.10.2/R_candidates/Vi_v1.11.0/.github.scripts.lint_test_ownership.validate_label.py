def validate_label(label: str, pytorch_labels: List[str]) -> str:
    if label not in pytorch_labels:
        return f"{label} is not a PyTorch label (please choose from https://github.com/pytorch/pytorch/labels)"
    if label.startswith("module:") or label.startswith("oncall:") or label in ACCEPTABLE_OWNER_LABELS:
        return ""
    return f"{label} is not an acceptable owner (please update to another label or edit ACCEPTABLE_OWNERS_LABELS " \
        "in {CURRENT_FILE_NAME}"
