    def __init__(
        self,
        elements: list[str],
        tag: str,
        attributes: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.elements = elements
        self.attributes = attributes
