    def get_child_images(self) -> list[ImageFile.ImageFile]:
        from . import ImageFile

        deprecate("Image.Image.get_child_images", 13)
        return ImageFile.ImageFile.get_child_images(self)  # type: ignore[arg-type]
