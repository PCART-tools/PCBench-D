        def send_json(self, content):
            self.write_message(json.dumps(content))
