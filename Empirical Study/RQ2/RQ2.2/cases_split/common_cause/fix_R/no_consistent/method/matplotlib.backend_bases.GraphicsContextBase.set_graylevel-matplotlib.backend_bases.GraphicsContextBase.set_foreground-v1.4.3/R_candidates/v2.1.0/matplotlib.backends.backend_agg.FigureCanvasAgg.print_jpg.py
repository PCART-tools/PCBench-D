        def print_jpg(self, filename_or_obj, *args, **kwargs):
            """
            Other Parameters
            ----------------
            quality : int
                The image quality, on a scale from 1 (worst) to
                95 (best). The default is 95, if not given in the
                matplotlibrc file in the savefig.jpeg_quality parameter.
                Values above 95 should be avoided; 100 completely
                disables the JPEG quantization stage.

            optimize : bool
                If present, indicates that the encoder should
                make an extra pass over the image in order to select
                optimal encoder settings.

            progressive : bool
                If present, indicates that this image
                should be stored as a progressive JPEG file.
            """
            buf, size = self.print_to_buffer()
            if kwargs.pop("dryrun", False):
                return
            # The image is "pasted" onto a white background image to safely
            # handle any transparency
            image = Image.frombuffer('RGBA', size, buf, 'raw', 'RGBA', 0, 1)
            rgba = mcolors.to_rgba(rcParams['savefig.facecolor'])
            color = tuple([int(x * 255.0) for x in rgba[:3]])
            background = Image.new('RGB', size, color)
            background.paste(image, image)
            options = {k: kwargs[k]
                       for k in ['quality', 'optimize', 'progressive', 'dpi']
                       if k in kwargs}
            options.setdefault('quality', rcParams['savefig.jpeg_quality'])
            if 'dpi' in options:
                # Set the same dpi in both x and y directions
                options['dpi'] = (options['dpi'], options['dpi'])

            return background.save(filename_or_obj, format='jpeg', **options)
