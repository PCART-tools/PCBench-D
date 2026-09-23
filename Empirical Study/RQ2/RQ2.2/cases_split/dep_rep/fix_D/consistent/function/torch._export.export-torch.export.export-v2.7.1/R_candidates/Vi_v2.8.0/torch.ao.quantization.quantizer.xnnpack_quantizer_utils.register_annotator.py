def register_annotator(op: str) -> Callable[[AnnotatorType], None]:
    def decorator(annotator: AnnotatorType) -> None:
        OP_TO_ANNOTATOR[op] = annotator

    return decorator
