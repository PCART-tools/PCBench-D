def update_equation(
    symints: list[Union[torch.SymInt, int]],
    init_symints: list[Union[torch.SymInt, int]],
    padding_constraints: defaultdict[torch.SymInt, list[Union[sp.Expr, int]]],
    init_eq: sp.Expr,
    new_mod_num: int,
    var: torch.SymInt,
    idx: int,
) -> None:
    padding_constraints[var].append(new_mod_num)
    mod_num = np.lcm.reduce(padding_constraints[var][1:])  # type: ignore[arg-type]
    eq = mod_num * init_symints[idx]
    eq_const = [arg for arg in init_eq.args if arg.is_number]
    if eq_const:
        rem = int(eq_const[0] % mod_num)
        eq -= rem
    symints[idx] = eq
