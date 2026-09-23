    def __init__(
        self, env, engine, parser, preparser=lambda source, f=None: source
    ) -> None:
        super().__init__(env, engine, parser, preparser=preparser)
