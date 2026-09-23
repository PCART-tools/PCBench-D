    def show_image(self, image: Image.Image, **options: Any) -> int:
        """Display the given image."""
        return self.show_file(self.save_image(image), **options)
