        def get_length(self) -> int:
            headers = self.render_headers()
            data = self.render_data()
            return len(headers) + len(data)
