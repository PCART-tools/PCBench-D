    def send_json(self, data, *, dumps=json.dumps):
        self.send_str(dumps(data))
