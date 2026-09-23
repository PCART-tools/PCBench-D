    def get_window_extent(self, renderer):
        # TODO:check to ensure that this does not fail for
        # cases other than scatter plot legend
        return self.get_datalim(transforms.IdentityTransform())
