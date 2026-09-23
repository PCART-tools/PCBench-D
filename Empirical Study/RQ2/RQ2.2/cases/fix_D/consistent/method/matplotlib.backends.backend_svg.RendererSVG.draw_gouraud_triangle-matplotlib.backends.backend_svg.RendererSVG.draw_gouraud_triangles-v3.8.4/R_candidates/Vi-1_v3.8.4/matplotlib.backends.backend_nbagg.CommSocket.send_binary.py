    def send_binary(self, blob):
        if self.supports_binary:
            self.comm.send({'blob': 'image/png'}, buffers=[blob])
        else:
            # The comm is ASCII, so we send the image in base64 encoded data
            # URL form.
            data = b64encode(blob).decode('ascii')
            data_uri = f"data:image/png;base64,{data}"
            self.comm.send({'data': data_uri})
