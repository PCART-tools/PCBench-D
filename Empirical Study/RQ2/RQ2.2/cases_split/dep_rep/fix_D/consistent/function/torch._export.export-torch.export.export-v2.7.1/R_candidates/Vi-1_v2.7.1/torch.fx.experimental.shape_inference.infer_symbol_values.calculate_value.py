def calculate_value(
    left_expression: Union[str, Any, None],
    right_expression: Union[str, Any, None],
    symints: list[Union[torch.SymInt, int]],
    symbol_idx_dict: dict[str, int],
) -> None:
    var, val = solve_equation(left_expression, right_expression)
    idx = symbol_idx_dict[var]
    pre_equation = sp.sympify(f"{symints[idx]}")
    symints[idx] = pre_equation.subs(sp.sympify(var), val)
