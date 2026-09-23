    def _make_id(self, type, content):
        content = str(content)
        if rcParams['svg.hashsalt'] is None:
            salt = str(uuid.uuid4())
        else:
            salt = rcParams['svg.hashsalt']
        if six.PY3:
            content = content.encode('utf8')
            salt = salt.encode('utf8')
        m = md5()
        m.update(salt)
        m.update(content)
        return '%s%s' % (type, m.hexdigest()[:10])
