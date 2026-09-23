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

    class DistributeFunction(TorchFunctionMode):
        def __init__(
            self,
            fn: Callable,
            device_mesh: DeviceMesh,
            input_fn: Optional[Callable] = None,
            output_fn: Optional[Callable] = None,
        ):
            self._device_mesh = device_mesh
            self._input_fn = input_fn
            self._output_fn = output_fn
            self._fn = fn

        def __torch_function__(
            self,
            func: Callable,
            types: Any,
            args: tuple[Any, ...] = (),
            kwargs: Optional[dict[str, Any]] = None,
        ) -> Any:
            kwargs = kwargs or {}

            if func != self._fn:
                return func(*args, **kwargs)

            if self._input_fn is not None:
                args, kwargs = self._input_fn(self._device_mesh, *args, **kwargs)
            output = func(*args, **kwargs)
            if self._output_fn is not None:
                output = self._output_fn(self._device_mesh, output)
            return output

    if _dispatch_mode == _DispatchMode.MONKEY_PATCH:
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
    elif _dispatch_mode == _DispatchMode.TORCH_FUNCTION:
        with DistributeFunction(
            F.scaled_dot_product_attention,
            mesh,
            attention_input_fn,
            attention_output_fn,
        ):
            with _enable_cp_dispatcher():
                yield
    else:
        raise NotImplementedError("torch dispatch mode is not supported yet.")
