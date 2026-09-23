def get_validators() -> tuple[str, str]:
    r"""Return the TunableOp validators."""
    return torch._C._cuda_tunableop_get_validators()  # type: ignore[attr-defined]
