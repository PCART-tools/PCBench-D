        def send_binary(self, blob):
            if self.supports_binary:
                self.write_message(blob, binary=True)
            else:
                data_uri = "data:image/png;base64,{}".format(
                    blob.encode('base64').replace('\n', ''))
                self.write_message(data_uri)
