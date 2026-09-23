    def create_options(self):
        options = self.import_options(self.browser)()
        if self.headless:
            match self.browser:
                case "chrome" | "edge":
                    options.add_argument("--headless=new")
                case "firefox":
                    options.add_argument("-headless")
        return options
