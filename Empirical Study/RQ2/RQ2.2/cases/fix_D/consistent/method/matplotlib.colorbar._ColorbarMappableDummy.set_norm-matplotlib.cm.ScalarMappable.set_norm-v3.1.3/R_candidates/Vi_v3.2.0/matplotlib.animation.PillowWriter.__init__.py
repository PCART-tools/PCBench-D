    def __init__(self, *args, **kwargs):
        if kwargs.get("extra_args") is None:
            kwargs["extra_args"] = ()
        super().__init__(*args, **kwargs)
