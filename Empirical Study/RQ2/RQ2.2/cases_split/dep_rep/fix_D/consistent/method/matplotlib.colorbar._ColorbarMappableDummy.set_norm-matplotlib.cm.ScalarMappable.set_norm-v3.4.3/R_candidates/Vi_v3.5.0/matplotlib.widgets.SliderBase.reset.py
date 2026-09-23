    def reset(self):
        """Reset the slider to the initial value."""
        if np.any(self.val != self.valinit):
            self.set_val(self.valinit)
