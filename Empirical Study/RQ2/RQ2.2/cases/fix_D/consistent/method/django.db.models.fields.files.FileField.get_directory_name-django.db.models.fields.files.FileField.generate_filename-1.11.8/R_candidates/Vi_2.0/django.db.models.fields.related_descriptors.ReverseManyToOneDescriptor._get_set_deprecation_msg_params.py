    def _get_set_deprecation_msg_params(self):
        return (
            'reverse side of a related set',
            self.rel.get_accessor_name(),
        )
