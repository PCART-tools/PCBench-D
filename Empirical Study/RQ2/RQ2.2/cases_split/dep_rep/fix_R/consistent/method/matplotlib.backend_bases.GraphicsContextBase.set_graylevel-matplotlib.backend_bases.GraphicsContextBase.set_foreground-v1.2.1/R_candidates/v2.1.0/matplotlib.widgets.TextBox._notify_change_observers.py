    def _notify_change_observers(self):
        for cid, func in six.iteritems(self.change_observers):
            func(self.text)
