    def copy(self, alias=None, allow_thread_sharing=None):
        """
        Return a copy of this connection.

        For tests that require two connections to the same database.
        """
        settings_dict = copy.deepcopy(self.settings_dict)
        if alias is None:
            alias = self.alias
        if allow_thread_sharing is None:
            allow_thread_sharing = self.allow_thread_sharing
        return type(self)(settings_dict, alias, allow_thread_sharing)
