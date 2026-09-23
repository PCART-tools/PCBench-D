    def _need_parse_response_body(self):
        return (self.method.lower() != 'head' and
                self.status not in [204, 304])
