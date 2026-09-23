def _parse_domain_op_type(domain_op: str) -> tuple[str, str]:
    splitted = domain_op.split("::", 1)
    if len(splitted) == 1:
        domain = ""
        op_type = splitted[0]
    else:
        domain = splitted[0]
        op_type = splitted[1]
    return domain, op_type
