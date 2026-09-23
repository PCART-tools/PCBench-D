    def raise_for_status(self):
        if 400 <= self.status:
            raise ClientResponseError(
                self.request_info,
                self.history,
                code=self.status,
                message=self.reason,
                headers=self.headers)
