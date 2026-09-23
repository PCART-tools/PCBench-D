    def _notify_submit_observers(self):
        for cid, func in six.iteritems(self.submit_observers):
                func(self.text)
