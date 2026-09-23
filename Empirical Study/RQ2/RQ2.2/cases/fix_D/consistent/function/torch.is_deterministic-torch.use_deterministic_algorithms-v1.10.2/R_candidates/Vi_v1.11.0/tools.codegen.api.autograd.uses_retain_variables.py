def uses_retain_variables(info: Optional[DifferentiabilityInfo]) -> bool:
    return uses_ident(info, 'retain_variables')
