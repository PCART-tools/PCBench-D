        def print_jpg(self, filename_or_obj, *args, dryrun=False,
                      pil_kwargs=None, **kwargs):
            """
            Write the figure to a JPEG file.

            Parameters
            ----------
            filename_or_obj : str or PathLike or file-like object
                The file to write to.

            Other Parameters
            ----------------
            quality : int
                The image quality, on a scale from 1 (worst) to 100 (best).
                The default is :rc:`savefig.jpeg_quality`.  Values above
                95 should be avoided; 100 completely disables the JPEG
                quantization stage.

            optimize : bool
                If present, indicates that the encoder should
                make an extra pass over the image in order to select
                optimal encoder settings.

            progressive : bool
                If present, indicates that this image
                should be stored as a progressive JPEG file.

            pil_kwargs : dict, optional
                Additional keyword arguments that are passed to
                `PIL.Image.save` when saving the figure.  These take precedence
                over *quality*, *optimize* and *progressive*.
            """
            buf, size = self.print_to_buffer()
            if dryrun:
                return
            # The image is "pasted" onto a white background image to safely
            # handle any transparency
            image = Image.frombuffer('RGBA', size, buf, 'raw', 'RGBA', 0, 1)
            rgba = mcolors.to_rgba(rcParams['savefig.facecolor'])
            color = tuple([int(x * 255) for x in rgba[:3]])
            background = Image.new('RGB', size, color)
            background.paste(image, image)
            if pil_kwargs is None:
                pil_kwargs = {}
            for k in ["quality", "optimize", "progressive"]:
                if k in kwargs:
                    pil_kwargs.setdefault(k, kwargs[k])
            pil_kwargs.setdefault("quality", rcParams["savefig.jpeg_quality"])
            pil_kwargs.setdefault("dpi", (self.figure.dpi, self.figure.dpi))
            return background.save(
                filename_or_obj, format='jpeg', **pil_kwargs)
