    def __call__(self, *args, **kwargs):
        if len(kwargs) > 0 and len(args) > 0:
            raise ValueError("Pipeline cannot handle mixed args and kwargs")

        if len(kwargs) > 0:
            return DefaultArgumentHandler.handle_kwargs(kwargs)
        else:
            return DefaultArgumentHandler.handle_args(args)
