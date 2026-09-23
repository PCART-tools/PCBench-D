    def adjoin(self, space: int, *lists, **kwargs) -> str:
        return printing.adjoin(
            space, *lists, strlen=self.len, justfunc=self.justify, **kwargs
        )
