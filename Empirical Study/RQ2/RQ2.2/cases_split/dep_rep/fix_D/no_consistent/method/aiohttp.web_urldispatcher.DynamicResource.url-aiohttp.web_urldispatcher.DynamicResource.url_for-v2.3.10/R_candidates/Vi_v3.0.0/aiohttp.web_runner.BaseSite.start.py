    @abstractmethod
    async def start(self):
        self._runner._reg_site(self)
