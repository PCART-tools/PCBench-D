def webdriver_test(testfunc):
    @functools.wraps(testfunc)
    def wrapper(self, *args, **kwds):
        self.needs_resources()

        if os.environ.get("RUN_WEBDRIVER") != "1":
            self.skipTest("Webdriver not requested")
        from selenium import webdriver

        for driver in [
                "Firefox",
                "Chrome",
        ]:
            with self.subTest(driver=driver):
                wd = getattr(webdriver, driver)()
                testfunc(self, wd, *args, **kwds)
                wd.close()

    return wrapper
