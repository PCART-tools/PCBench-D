    def _gen_form_urlencoded(self):
        # form data (x-www-form-urlencoded)
        data = []
        for type_options, _, value in self._fields:
            data.append((type_options['name'], value))

        charset = self._charset if self._charset is not None else 'utf-8'
        return payload.BytesPayload(
            urlencode(data, doseq=True).encode(charset),
            content_type='application/x-www-form-urlencoded')
