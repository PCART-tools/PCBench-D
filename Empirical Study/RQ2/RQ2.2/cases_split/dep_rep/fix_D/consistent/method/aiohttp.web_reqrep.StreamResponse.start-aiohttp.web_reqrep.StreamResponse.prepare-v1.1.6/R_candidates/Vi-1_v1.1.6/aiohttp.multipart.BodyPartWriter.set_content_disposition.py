    def set_content_disposition(self, disptype, **params):
        """Sets ``Content-Disposition`` header.

        :param str disptype: Disposition type: inline, attachment, form-data.
                            Should be valid extension token (see RFC 2183)
        :param dict params: Disposition params
        """
        if not disptype or not (TOKEN > set(disptype)):
            raise ValueError('bad content disposition type {!r}'
                             ''.format(disptype))
        value = disptype
        if params:
            lparams = []
            for key, val in params.items():
                if not key or not (TOKEN > set(key)):
                    raise ValueError('bad content disposition parameter'
                                     ' {!r}={!r}'.format(key, val))
                qval = quote(val, '')
                lparams.append((key, '"%s"' % qval))
                if key == 'filename':
                    lparams.append(('filename*', "utf-8''" + qval))
            sparams = '; '.join('='.join(pair) for pair in lparams)
            value = '; '.join((value, sparams))
        self.headers[CONTENT_DISPOSITION] = value
