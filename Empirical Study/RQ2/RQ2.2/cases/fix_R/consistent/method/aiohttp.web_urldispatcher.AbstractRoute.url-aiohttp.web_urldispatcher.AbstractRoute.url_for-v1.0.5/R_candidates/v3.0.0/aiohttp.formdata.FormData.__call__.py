    def __call__(self):
        if self._is_multipart:
            return self._gen_form_data()
        else:
            return self._gen_form_urlencoded()
