def trace_structured_artifact(
    name: str,  # this will go in metadata
    encoding: str,
    payload_fn: Callable[[], Optional[Union[str, object]]] = lambda: None,
) -> None:
    trace_structured(
        "artifact",
        metadata_fn=lambda: {
            "name": name,
            "encoding": encoding,
        },
        payload_fn=payload_fn,
    )
