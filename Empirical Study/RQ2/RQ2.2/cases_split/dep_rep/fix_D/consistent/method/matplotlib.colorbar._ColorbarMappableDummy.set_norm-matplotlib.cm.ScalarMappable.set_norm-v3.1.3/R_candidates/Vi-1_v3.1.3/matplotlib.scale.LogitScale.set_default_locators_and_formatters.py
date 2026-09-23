    def set_default_locators_and_formatters(self, axis):
        # ..., 0.01, 0.1, 0.5, 0.9, 0.99, ...
        axis.set_major_locator(LogitLocator())
        axis.set_major_formatter(LogitFormatter())
        axis.set_minor_locator(LogitLocator(minor=True))
        axis.set_minor_formatter(LogitFormatter())
