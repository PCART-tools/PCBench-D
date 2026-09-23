    def __init__(
        self, patterns: list[str] | None = None, op_name: str | None = None
    ) -> None:
        if patterns is not None:
            self.patterns = patterns
        else:
            self.patterns = []
        self.lut: bytearray | None = None
        if op_name is not None:
            known_patterns = {
                "corner": ["1:(... ... ...)->0", "4:(00. 01. ...)->1"],
                "dilation4": ["4:(... .0. .1.)->1"],
                "dilation8": ["4:(... .0. .1.)->1", "4:(... .0. ..1)->1"],
                "erosion4": ["4:(... .1. .0.)->0"],
                "erosion8": ["4:(... .1. .0.)->0", "4:(... .1. ..0)->0"],
                "edge": [
                    "1:(... ... ...)->0",
                    "4:(.0. .1. ...)->1",
                    "4:(01. .1. ...)->1",
                ],
            }
            if op_name not in known_patterns:
                msg = f"Unknown pattern {op_name}!"
                raise Exception(msg)

            self.patterns = known_patterns[op_name]
