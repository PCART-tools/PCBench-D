    def __init__(
        self,
        env,
        engine,
        parser,
        preparser=partial(
            _preparse,
            f=_compose(
                _replace_locals, _replace_booleans, _clean_spaces_backtick_quoted_names
            ),
        ),
    ):
        super().__init__(env, engine, parser, preparser)
