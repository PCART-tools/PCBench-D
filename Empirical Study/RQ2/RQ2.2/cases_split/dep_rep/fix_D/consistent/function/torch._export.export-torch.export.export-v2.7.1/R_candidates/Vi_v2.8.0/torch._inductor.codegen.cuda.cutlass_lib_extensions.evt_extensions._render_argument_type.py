    def _render_argument_type(
        epilogue_functor: EpilogueFunctor,
        name_to_buffer: dict[str, Buffer],
        size_hint_fn: Callable[[Union[Expr, int]], int],
    ) -> str:
        epilogue_thread_type = epilogue_functor.epilogue_thread_type

        # Fragile, but this is the only way to guarantee t is expected type because t is a local class
        def is_nested_visitor_type(t: type) -> bool:
            return (
                ".".join([t.__module__, t.__qualname__])
                == "cutlass.backend.c_types.visitor_factory.<locals>.VisitorType"
            )

        buffer = IndentedBuffer()
        with buffer.set_tabwidth(2):

            def render_argument_type(name: str, t: CutlassArgType) -> None:
                if issubclass(t, ctypes.c_byte):
                    buffer.writeline(f"{{}}, /* {name} */")
                else:
                    fields = [
                        (
                            fname,
                            _get_arg_from_node(ty, name_to_buffer[name], size_hint_fn),
                        )
                        for fname, ty in t._fields_
                    ]
                    field_strs = [
                        f"/* {fname} */ {str(field)}" for fname, field in fields
                    ]
                    buffer.writeline(f"{{{', '.join(field_strs)}}}, /* {name} */")

            def render_thread_type(name: str, t: CutlassArgType) -> None:
                if is_nested_visitor_type(t):
                    buffer.writeline(f"{{ /* {name} */")
                    with buffer.indent():
                        for name, inner_t in t._fields_:
                            render_thread_type(name, inner_t)
                    buffer.writeline("},")
                else:
                    render_argument_type(name, t)

            # unroll the recursion once to address special case formatting
            # namely, no ending comma and no indentation for the outermost thread type
            buffer.writeline("{ /* thread */")
            with buffer.indent(3):
                if is_nested_visitor_type(epilogue_thread_type):
                    with buffer.indent():
                        for name, inner_t in epilogue_thread_type._fields_:
                            render_thread_type(name, inner_t)
                else:
                    render_argument_type("thread", epilogue_thread_type)
                buffer.writeline("}")

        return buffer.getvalue()
