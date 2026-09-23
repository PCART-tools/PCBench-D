def make_column(
    *,
    data: Optional[Report],
    filename: Optional[str],
    suite_name: Optional[str],
    test_name: str,
    digits: int,
) -> Tuple[str, int]:
    decimals = 3
    num_length = digits + 1 + decimals
    if data:
        cases = get_cases(
            data=data,
            filename=filename,
            suite_name=suite_name,
            test_name=test_name
        )
        if cases:
            case = cases[0]
            status = case['status']
            omitted = len(cases) - 1
            if status:
                return f'{status.rjust(num_length)} ', omitted
            else:
                return f'{case["seconds"]:{num_length}.{decimals}f}s', omitted
        else:
            return f'{"absent".rjust(num_length)} ', 0
    else:
        return ' ' * (num_length + 1), 0
