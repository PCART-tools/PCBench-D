    def send_json(self, content):
        self.comm.send({'data': json.dumps(content)})
