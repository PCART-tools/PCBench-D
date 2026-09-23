    @classmethod
    def get_capability(cls, browser):
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

        return getattr(DesiredCapabilities, browser.upper())
