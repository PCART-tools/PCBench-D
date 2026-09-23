def section(msg: str) -> None:
    if rank == 0:
        rich.print(rich.rule.Rule(msg))
