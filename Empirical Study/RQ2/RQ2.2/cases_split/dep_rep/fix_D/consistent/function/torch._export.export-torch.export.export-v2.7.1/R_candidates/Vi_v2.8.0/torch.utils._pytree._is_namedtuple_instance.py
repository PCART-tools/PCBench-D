@deprecated(
    "torch.utils._pytree._is_namedtuple_instance is private and will be removed in a future release. "
    "Please use torch.utils._pytree.is_namedtuple_instance instead.",
    category=FutureWarning,
)
def _is_namedtuple_instance(tree: Any) -> bool:
    return is_namedtuple_instance(tree)
