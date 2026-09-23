@substitute_in_graph(operator.itemgetter, is_embedded_type=True)  # type: ignore[arg-type,misc]
def itemgetter(*items: Any) -> Callable[[Any], Any | tuple[Any, ...]]:
    if len(items) == 0:
        raise TypeError("itemgetter expected 1 argument, got 0")

    if len(items) == 1:
        item = items[0]

        def getter(obj: Any) -> Any:
            return obj[item]

    else:

        def getter(obj: Any) -> tuple[Any, ...]:  # type: ignore[misc]
            return tuple(obj[item] for item in items)

    return getter
