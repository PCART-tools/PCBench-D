    def presign_and_upload(self, token: str, filename: str, filepath: str, organization: Optional[str] = None) -> str:
        """
        Get a presigned url, then upload file to S3.

        Outputs:
            url: Read-only url for the stored file on S3.
        """
        urls = self.presign(token, filename=filename, organization=organization)
        # streaming upload:
        # https://2.python-requests.org/en/master/user/advanced/#streaming-uploads
        #
        # Even though we presign with the correct content-type,
        # the client still has to specify it when uploading the file.
        with open(filepath, "rb") as f:
            pf = TqdmProgressFileReader(f)
            data = f if pf.total_size > 0 else ""

            r = requests.put(urls.write, data=data, headers={"content-type": urls.type})
            r.raise_for_status()
            pf.close()
        return urls.access
