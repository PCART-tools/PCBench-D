    def __init__(self, env, engine, parser, preparser=lambda x: x):
        super(PythonExprVisitor, self).__init__(env, engine, parser,
                                                preparser=preparser)
