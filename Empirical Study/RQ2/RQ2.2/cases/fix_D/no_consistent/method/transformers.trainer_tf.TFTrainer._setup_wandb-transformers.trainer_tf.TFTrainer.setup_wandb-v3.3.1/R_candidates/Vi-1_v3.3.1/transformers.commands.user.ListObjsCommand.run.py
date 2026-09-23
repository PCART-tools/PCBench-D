    def run(self):
        token = HfFolder.get_token()
        if token is None:
            print("Not logged in")
            exit(1)
        try:
            objs = self._api.list_objs(token, organization=self.args.organization)
        except HTTPError as e:
            print(e)
            print(ANSI.red(e.response.text))
            exit(1)
        if len(objs) == 0:
            print("No shared file yet")
            exit()
        rows = [[obj.filename, obj.LastModified, obj.ETag, obj.Size] for obj in objs]
        print(self.tabulate(rows, headers=["Filename", "LastModified", "ETag", "Size"]))
