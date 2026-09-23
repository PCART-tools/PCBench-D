    def runshell(self):
        args = [self.executable_name,
                self.connection.settings_dict['NAME']]
        subprocess.check_call(args)
