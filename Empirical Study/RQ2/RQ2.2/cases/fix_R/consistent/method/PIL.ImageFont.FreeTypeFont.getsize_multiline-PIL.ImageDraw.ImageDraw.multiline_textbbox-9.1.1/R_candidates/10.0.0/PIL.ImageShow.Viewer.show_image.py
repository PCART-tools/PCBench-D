    def show_image(self, image, **options):
        """Display the given image."""
        return self.show_file(self.save_image(image), **options)
