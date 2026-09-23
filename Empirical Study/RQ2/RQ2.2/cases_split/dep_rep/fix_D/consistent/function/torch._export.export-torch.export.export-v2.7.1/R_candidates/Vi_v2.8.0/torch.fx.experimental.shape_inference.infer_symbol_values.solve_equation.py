def solve_equation(
    left_expression: Union[str, Any, None],
    right_expression: Union[str, Any, None],
) -> tuple[str, int]:
    expression = f"{left_expression} - {right_expression}"
    var = re.findall(s_pattern, expression)[0]
    if re.findall(parentheses_pattern, expression):
        sub_expression = re.findall(parentheses_pattern, expression)[0]
        var, coeff = sub_expression.split("//")
        x = sp.symbols("x")
        sub_equation = sp.sympify(f"{var} - {coeff} * {x}")
        modified_equation = (
            sp.sympify(x) + sp.sympify(expression) - sp.sympify(sub_expression)
        )

        solution = sp.solve((modified_equation, sub_equation), (x, var))
        return (var, int(solution[sp.sympify(var)]))
    else:
        solution = sp.solve(expression, var)
        val = int(solution[0])
        return (var, val)
