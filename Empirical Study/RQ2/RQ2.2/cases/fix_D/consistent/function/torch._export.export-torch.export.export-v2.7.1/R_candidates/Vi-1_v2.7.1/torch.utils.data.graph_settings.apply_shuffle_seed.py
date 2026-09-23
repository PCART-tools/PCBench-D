@deprecated(
    "`apply_shuffle_seed` is deprecated since 1.12 and will be removed in the future releases. "
    "Please use `apply_random_seed` instead.",
    category=FutureWarning,
)
def apply_shuffle_seed(datapipe: DataPipe, rng: Any) -> DataPipe:
    return apply_random_seed(datapipe, rng)
