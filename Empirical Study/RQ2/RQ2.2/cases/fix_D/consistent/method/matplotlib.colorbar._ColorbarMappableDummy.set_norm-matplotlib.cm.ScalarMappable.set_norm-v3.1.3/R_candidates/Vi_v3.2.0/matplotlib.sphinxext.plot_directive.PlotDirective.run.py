    def run(self):
        """Run the plot directive."""
        return run(self.arguments, self.content, self.options,
                   self.state_machine, self.state, self.lineno)
