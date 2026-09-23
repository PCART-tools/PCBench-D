    def get_results(self, box, used_characters):
        ship(0, 0, box)
        return (self.width,
                self.height + self.depth,
                self.depth,
                self.pswriter,
                used_characters)
