    def __init__(self, env, engine, parser,
                 preparser=partial(_preparse, f=_compose(_replace_locals,
                                                         _replace_booleans))):
        super(PandasExprVisitor, self).__init__(env, engine, parser, preparser)
