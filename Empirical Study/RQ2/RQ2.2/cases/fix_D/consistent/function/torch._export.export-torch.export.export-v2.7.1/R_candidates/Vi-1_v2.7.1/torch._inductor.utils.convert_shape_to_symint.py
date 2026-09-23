def convert_shape_to_symint(
    lst: Iterable[Union[int, sympy.Expr]],
) -> list[Union[int, torch.SymInt]]:
    """
    Takes a list of shapes from Inductor and converts them into symints (or just
    ints if all shapes are static).
    """
    from .virtualized import V

    return [
        (
            i
            if isinstance(i, int)
            else (
                int(i)
                if isinstance(i, sympy.Integer)
                else V.graph.sizevars.shape_env.create_symintnode(i, hint=None)
            )
        )
        for i in lst
    ]
