def _optimized_add(
    lhs, rhs, lhs_is_optimized_summation=False, rhs_is_optimized_summation=False
):
    """
    Custom optimization for Add used to optimize incremental binary summations of certain properties. The idea
    is when we know the expression is a summation of unique symbols all we need to know is the correct order of symbols,
    and no other optimizations are needed. We pass evaluate=false, with the correct order of args and save the following.
    1. Avoid running other optimizations when the Add is constructed.
    2. Manually figure out the order of the args for the new expression in log(n) comparisons instead of nLog(n)
    (comparing terms is expensive and shows in the profiles).
    The function returns a tuple of (1) a boolean that indicates whether the output is a summation of unique symbols,
    (2) the result sympy expression.
    """
    import sympy
    from sympy.core.basic import _args_sortkey as sortkey

    def make_optimized(ordered_args):
        result = sympy.Add(*ordered_args, evaluate=False)
        return (True, result)

    from torch.utils._sympy.functions import _is_symbols_binary_summation

    lhs_is_optimized_summation |= _is_symbols_binary_summation(lhs)
    rhs_is_optimized_summation |= _is_symbols_binary_summation(rhs)

    if lhs_is_optimized_summation and rhs_is_optimized_summation:
        # (a0+a1..) + (a2+a3..) => (a0+a1+a2+a3)
        if sortkey(lhs._args[-1]) < sortkey(rhs._args[0]):
            return make_optimized(lhs._args + rhs._args)
        #  (a2+a3..) + (a0+a1..) => (a0+a1+a2+a3)
        if sortkey(lhs._args[0]) > sortkey(rhs._args[-1]):
            return make_optimized(rhs._args + lhs._args)

    # (a0+a2) + a1 => (a0+a1+a2)
    if lhs_is_optimized_summation and rhs.is_symbol:
        new_args = _binary_search_insert_arg(list(lhs._args), rhs)
        if new_args is not None:
            return make_optimized(new_args)

    # a1 + (a0+a2)=> (a0+a1+a2)
    if rhs_is_optimized_summation and lhs.is_symbol:
        new_args = _binary_search_insert_arg(list(rhs._args), lhs)
        if new_args is not None:
            return make_optimized(new_args)

    result = sympy.Add(lhs, rhs)
    return (_is_symbols_binary_summation(result), result)
