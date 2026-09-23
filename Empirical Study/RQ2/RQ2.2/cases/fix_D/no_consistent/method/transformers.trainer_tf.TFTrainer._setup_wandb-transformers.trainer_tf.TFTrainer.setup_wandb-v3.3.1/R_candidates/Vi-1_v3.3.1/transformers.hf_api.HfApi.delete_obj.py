    def delete_obj(self, token: str, filename: str, organization: Optional[str] = None):
        """
        Call HF API to delete a file stored by user
        """
        path = "{}/api/deleteObj".format(self.endpoint)
        r = requests.delete(
            path,
            headers={"authorization": "Bearer {}".format(token)},
            json={"filename": filename, "organization": organization},
        )
        r.raise_for_status()
