    def raise_for_status(self):
        if 400 <= self.status:
            raise ClientResponseError(
                code=self.status,
                message=self.reason,
                headers=self.headers)
