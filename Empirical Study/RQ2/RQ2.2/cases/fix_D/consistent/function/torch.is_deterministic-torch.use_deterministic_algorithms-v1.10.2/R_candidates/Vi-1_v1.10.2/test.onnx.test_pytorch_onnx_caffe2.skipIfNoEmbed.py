def skipIfNoEmbed(func):
    def wrapper(self):
        if not self.embed_params:
            raise unittest.SkipTest("Skip debug embed_params test")
        return func(self)
    return wrapper
