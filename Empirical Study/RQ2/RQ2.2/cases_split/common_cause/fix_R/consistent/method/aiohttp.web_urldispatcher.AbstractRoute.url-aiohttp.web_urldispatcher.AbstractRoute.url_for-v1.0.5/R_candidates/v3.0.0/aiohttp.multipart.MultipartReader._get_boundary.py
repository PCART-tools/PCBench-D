    def _get_boundary(self):
        mimetype = parse_mimetype(self.headers[CONTENT_TYPE])

        assert mimetype.type == 'multipart', (
            'multipart/* content type expected'
        )

        if 'boundary' not in mimetype.parameters:
            raise ValueError('boundary missed for Content-Type: %s'
                             % self.headers[CONTENT_TYPE])

        boundary = mimetype.parameters['boundary']
        if len(boundary) > 70:
            raise ValueError('boundary %r is too long (70 chars max)'
                             % boundary)

        return boundary
