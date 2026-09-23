    def save_image(self, image: Image.Image) -> str:
        """Save to temporary file and return filename."""
        return image._dump(format=self.get_format(image), **self.options)
