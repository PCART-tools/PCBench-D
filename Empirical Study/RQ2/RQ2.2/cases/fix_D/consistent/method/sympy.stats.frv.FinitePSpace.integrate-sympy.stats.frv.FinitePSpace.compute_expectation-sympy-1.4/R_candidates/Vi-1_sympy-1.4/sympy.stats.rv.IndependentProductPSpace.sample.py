    def sample(self):
        return {k: v for space in self.spaces
            for k, v in space.sample().items()}
