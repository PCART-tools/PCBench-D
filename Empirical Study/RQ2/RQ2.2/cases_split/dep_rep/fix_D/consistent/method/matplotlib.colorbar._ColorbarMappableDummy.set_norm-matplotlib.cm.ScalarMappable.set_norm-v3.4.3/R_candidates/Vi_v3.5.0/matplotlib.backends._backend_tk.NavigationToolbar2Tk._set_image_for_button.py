    def _set_image_for_button(self, button):
        """
        Set the image for a button based on its pixel size.

        The pixel size is determined by the DPI scaling of the window.
        """
        if button._image_file is None:
            return

        size = button.winfo_pixels('18p')
        with Image.open(button._image_file.replace('.png', '_large.png')
                        if size > 24 else button._image_file) as im:
            image = ImageTk.PhotoImage(im.resize((size, size)), master=self)
        button.configure(image=image, height='18p', width='18p')
        button._ntimage = image  # Prevent garbage collection.
