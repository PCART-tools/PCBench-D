def _scalar_str(self, formatter1, formatter2=None):
    if formatter2 is not None:
        real_str = _scalar_str(self.real, formatter1)
        imag_str = (_scalar_str(self.imag, formatter2) + "j").lstrip()
        # handles negative numbers, +0.0, -0.0
        if imag_str[0] == "+" or imag_str[0] == "-":
            return real_str + imag_str
        else:
            return real_str + "+" + imag_str
    else:
        return formatter1.format(self.item())
