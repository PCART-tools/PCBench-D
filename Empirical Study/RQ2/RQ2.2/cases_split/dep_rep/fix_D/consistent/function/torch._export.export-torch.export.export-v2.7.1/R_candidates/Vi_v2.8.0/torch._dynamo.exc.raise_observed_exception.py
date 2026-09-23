def raise_observed_exception(
    exc_type: type[Exception],
    tx: InstructionTranslatorBase,
    *,
    args: Optional[list[Any]] = None,
    kwargs: Optional[dict[str, Any]] = None,
) -> NoReturn:
    from .variables import BuiltinVariable

    # CPython here raises an exception. Since there is no python code, we have to manually setup the exception
    # stack and raise the exception.
    exception_vt = BuiltinVariable(exc_type).call_function(tx, args or [], kwargs or {})  # type: ignore[arg-type]
    tx.exn_vt_stack.set_current_exception(exception_vt)
    raise observed_exception_map[exc_type]
