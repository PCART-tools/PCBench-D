def raise_args_mismatch(tx, name):
    raise_observed_exception(
        TypeError,
        tx,
        args=[ConstantVariable(f"wrong number of arguments for {name}() call")],
    )
