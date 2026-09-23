    def __arrow_ext_serialize__(self):
        metadata = {"subtype": str(self.subtype), "closed": self.closed}
        return json.dumps(metadata).encode()
