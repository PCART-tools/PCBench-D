def get_results() -> tuple[str, str, str, float]:
    r"""Return all TunableOp results."""
    return torch._C._cuda_tunableop_get_results()  # type: ignore[attr-defined]
