@contextlib.contextmanager
def _context_parallel(seq_dim: int, mesh: DeviceMesh) -> Generator[None, None, None]:
    """Replace SDPA with the CP-wrapped version and enable DTensor CP dispatcher."""

    def attention_input_fn(
        mesh: DeviceMesh, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> tuple[tuple[Any, ...], dict[str, Any]]:
        placement = [Shard(seq_dim)]
        all_args = []

        for arg in itertools.chain(args, kwargs.values()):
            if isinstance(arg, torch.Tensor) and not isinstance(arg, DTensor):
                arg = DTensor.from_local(arg, mesh, placement, run_check=False)

            all_args.append(arg)

        new_args = tuple(all_args[0 : len(args)])
        new_kwargs = dict(zip(kwargs.keys(), all_args[len(args) :]))
        return new_args, new_kwargs

    def attention_output_fn(mesh: DeviceMesh, outputs: Any) -> Any:
        new_outputs = []
        for output in [outputs] if isinstance(outputs, torch.Tensor) else outputs:
            output = output.to_local() if isinstance(output, DTensor) else output
            new_outputs.append(output)

        if isinstance(outputs, torch.Tensor):
            return new_outputs[0]

        return tuple(new_outputs)

    # TODO: provide a more robust way to replace SDPA.
    # Currently we use monkey patch to replace scaled_dot_product_attention with the
    # wrapped fn. This is okay if users do `import torch.nn.functional` but will not
    # work if users do `import torch.nn.functional.scaled_dot_product_attention`.
    _distribute_function(
        F.scaled_dot_product_attention,
        F,
        mesh,
        attention_input_fn,
        attention_output_fn,
    )

    with _enable_cp_dispatcher():
        yield

    _restore_function(F.scaled_dot_product_attention, F)
