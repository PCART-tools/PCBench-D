def execute(
    gm: GraphModule,
    *args: Unpack[Ts],
    executor: str = "aten",
    executor_parameters: Optional[dict] = None,
) -> Any:
    """
    Prototype ATen executor.

    Just executes the context's graph.
    """

    if executor == "aten":
        return gm.forward(*args)

    msg = f"Received unexpected value for 'executor': {executor}. Allowed values are: aten."
    raise ValueError(msg)
