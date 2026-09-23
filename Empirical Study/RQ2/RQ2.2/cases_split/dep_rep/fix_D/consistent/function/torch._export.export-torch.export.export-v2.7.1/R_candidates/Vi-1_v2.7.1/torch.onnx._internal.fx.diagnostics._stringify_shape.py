def _stringify_shape(shape: torch.Size | None) -> str:
    if shape is None:
        return ""
    return f"[{', '.join(str(x) for x in shape)}]"
