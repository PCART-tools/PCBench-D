def layout_or_default(layout: Optional[torch.layout]) -> torch.layout:
    return layout if layout is not None else torch.strided
