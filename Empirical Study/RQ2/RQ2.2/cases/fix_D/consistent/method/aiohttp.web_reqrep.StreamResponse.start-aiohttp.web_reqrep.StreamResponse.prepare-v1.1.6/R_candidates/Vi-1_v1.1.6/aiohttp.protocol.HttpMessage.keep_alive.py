    def keep_alive(self):
        if self.keepalive is None:
            if self.version < HttpVersion10:
                # keep alive not supported at all
                return False
            if self.version == HttpVersion10:
                if self.headers.get(hdrs.CONNECTION) == 'keep-alive':
                    return True
                else:  # no headers means we close for Http 1.0
                    return False
            else:
                return not self.closing
        else:
            return self.keepalive
