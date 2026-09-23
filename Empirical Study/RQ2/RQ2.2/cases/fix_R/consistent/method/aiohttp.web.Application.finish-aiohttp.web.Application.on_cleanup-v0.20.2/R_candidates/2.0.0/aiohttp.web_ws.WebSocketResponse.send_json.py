    def send_json(self, data, *, dumps=json.dumps):
        return self.send_str(dumps(data))
