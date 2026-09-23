    def __repr__(self):
        out = io.StringIO()
        ascii_encodable_url = str(self.url)
        if self.reason:
            ascii_encodable_reason = self.reason.encode('ascii',
                                                        'backslashreplace') \
                .decode('ascii')
        else:
            ascii_encodable_reason = self.reason
        print('<ClientResponse({}) [{} {}]>'.format(
            ascii_encodable_url, self.status, ascii_encodable_reason),
            file=out)
        print(self.headers, file=out)
        return out.getvalue()
