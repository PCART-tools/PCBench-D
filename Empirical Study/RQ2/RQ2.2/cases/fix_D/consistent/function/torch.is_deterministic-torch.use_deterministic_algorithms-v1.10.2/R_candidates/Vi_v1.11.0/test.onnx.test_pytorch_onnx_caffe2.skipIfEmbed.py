def skipIfEmbed(func):
    def wrapper(self):
        if self.embed_params:
            raise unittest.SkipTest("Skip embed_params verify test")
        return func(self)
    return wrapper
