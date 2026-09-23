    def init(self, args: tuple[Any, ...]) -> None:
        """
        Override to perform codec specific initialization

        :param args: Tuple of arg items from the tile entry
        :returns: None
        """
        self.args = args
