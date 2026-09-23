def uses_single_grad(info: Optional[DifferentiabilityInfo]) -> bool:
    return uses_ident(info, 'grad')
