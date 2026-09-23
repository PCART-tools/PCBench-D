    def _get_boundary(self):
        mtype, *_, params = parse_mimetype(self.headers[CONTENT_TYPE])

        assert mtype == 'multipart', 'multipart/* content type expected'

        if 'boundary' not in params:
            raise ValueError('boundary missed for Content-Type: %s'
                             % self.headers[CONTENT_TYPE])

        boundary = params['boundary']
        if len(boundary) > 70:
            raise ValueError('boundary %r is too long (70 chars max)'
                             % boundary)

        return boundary
