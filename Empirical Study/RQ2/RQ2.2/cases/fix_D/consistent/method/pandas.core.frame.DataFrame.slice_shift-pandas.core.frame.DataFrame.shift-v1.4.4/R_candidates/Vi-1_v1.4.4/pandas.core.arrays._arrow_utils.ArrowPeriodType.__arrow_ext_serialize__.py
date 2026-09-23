    def __arrow_ext_serialize__(self):
        metadata = {"freq": self.freq}
        return json.dumps(metadata).encode()
