def needs_functionalization(
    selector: SelectiveBuilder,
    f: NativeFunction,
) -> bool:
    return (selector.include_all_operators and
            (f.is_view_op or modifies_arguments(f)))
