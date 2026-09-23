    def reset_position(self):
        """Make the original position the active position"""
        pos = self.get_position(original=True)
        self.set_position(pos, which='active')
