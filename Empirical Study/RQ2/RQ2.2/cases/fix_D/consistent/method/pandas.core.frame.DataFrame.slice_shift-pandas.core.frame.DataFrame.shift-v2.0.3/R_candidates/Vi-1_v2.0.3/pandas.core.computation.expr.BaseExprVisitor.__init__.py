    def __init__(self, env, engine, parser, preparser=_preparse) -> None:
        self.env = env
        self.engine = engine
        self.parser = parser
        self.preparser = preparser
        self.assigner = None
