    def presign(self, token: str, filename: str, organization: Optional[str] = None) -> PresignedUrl:
        """
        Call HF API to get a presigned url to upload `filename` to S3.
        """
        path = "{}/api/presign".format(self.endpoint)
        r = requests.post(
            path,
            headers={"authorization": "Bearer {}".format(token)},
            json={"filename": filename, "organization": organization},
        )
        r.raise_for_status()
        d = r.json()
        return PresignedUrl(**d)
