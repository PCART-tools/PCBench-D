    def set_xscale(self, scale, *args, **kwargs):
        if scale != 'linear':
            raise NotImplementedError(
                "You can not set the xscale on a polar plot.")
