    def raise_for_status(self):
        if 400 <= self.status:
            raise aiohttp.HttpProcessingError(
                code=self.status,
                message=self.reason)
