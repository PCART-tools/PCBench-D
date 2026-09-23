    def _make_id(self, type, content):
        salt = mpl.rcParams['svg.hashsalt']
        if salt is None:
            salt = str(uuid.uuid4())
        m = hashlib.md5()
        m.update(salt.encode('utf8'))
        m.update(str(content).encode('utf8'))
        return '%s%s' % (type, m.hexdigest()[:10])
