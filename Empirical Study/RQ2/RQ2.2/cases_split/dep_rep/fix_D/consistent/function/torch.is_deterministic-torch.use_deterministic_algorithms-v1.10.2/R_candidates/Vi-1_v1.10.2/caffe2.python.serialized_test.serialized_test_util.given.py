def given(*given_args, **given_kwargs):
    def wrapper(f):
        hyp_func = hy.seed(0)(hy.settings(max_examples=1)(hy.given(*given_args, **given_kwargs)(f)))
        fixed_seed_func = hy.seed(0)(hy.settings(max_examples=1)(hy.given(
            *given_args, **given_kwargs)(f)))

        def func(self, *args, **kwargs):
            self.should_serialize = True
            fixed_seed_func(self, *args, **kwargs)
            self.should_serialize = False
            hyp_func(self, *args, **kwargs)
        return func
    return wrapper
