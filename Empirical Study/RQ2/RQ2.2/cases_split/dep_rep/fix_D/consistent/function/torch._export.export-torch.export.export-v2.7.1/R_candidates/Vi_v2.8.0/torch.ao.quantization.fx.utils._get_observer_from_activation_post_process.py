def _get_observer_from_activation_post_process(
    activation_post_process: Union[ObserverBase, FakeQuantizeBase],
) -> ObserverBase:
    """
    If `activation_post_process` is an observer, return the observer.
    If `activation_post_process` is a fake quantize, return the internal observer.
    """
    if isinstance(activation_post_process, ObserverBase):
        return activation_post_process
    else:
        assert isinstance(activation_post_process, FakeQuantizeBase)
        return activation_post_process.activation_post_process  # type: ignore[return-value]
