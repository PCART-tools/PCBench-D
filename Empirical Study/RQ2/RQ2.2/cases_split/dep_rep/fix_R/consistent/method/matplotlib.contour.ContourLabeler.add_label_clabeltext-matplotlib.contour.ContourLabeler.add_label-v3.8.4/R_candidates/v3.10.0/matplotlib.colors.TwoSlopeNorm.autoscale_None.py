    def autoscale_None(self, A):
        """
        Get vmin and vmax.

        If vcenter isn't in the range [vmin, vmax], either vmin or vmax
        is expanded so that vcenter lies in the middle of the modified range
        [vmin, vmax].
        """
        super().autoscale_None(A)
        if self.vmin >= self.vcenter:
            self.vmin = self.vcenter - (self.vmax - self.vcenter)
        if self.vmax <= self.vcenter:
            self.vmax = self.vcenter + (self.vcenter - self.vmin)
