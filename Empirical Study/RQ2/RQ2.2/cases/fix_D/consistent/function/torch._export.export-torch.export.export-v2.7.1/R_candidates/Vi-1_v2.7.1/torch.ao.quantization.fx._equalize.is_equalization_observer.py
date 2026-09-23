def is_equalization_observer(observer: nn.Module) -> bool:
    return isinstance(
        observer, (_InputEqualizationObserver, _WeightEqualizationObserver)
    )
