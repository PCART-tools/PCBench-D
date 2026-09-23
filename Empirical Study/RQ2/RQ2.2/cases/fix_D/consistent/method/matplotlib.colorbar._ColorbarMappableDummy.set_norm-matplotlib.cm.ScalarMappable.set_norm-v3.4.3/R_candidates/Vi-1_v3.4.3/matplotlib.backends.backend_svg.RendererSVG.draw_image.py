    def draw_image(self, gc, x, y, im, transform=None):
        # docstring inherited

        h, w = im.shape[:2]

        if w == 0 or h == 0:
            return

        attrib = {}
        clipid = self._get_clip(gc)
        if clipid is not None:
            # Can't apply clip-path directly to the image because the
            # image has a transformation, which would also be applied
            # to the clip-path
            self.writer.start('g', attrib={'clip-path': 'url(#%s)' % clipid})

        oid = gc.get_gid()
        url = gc.get_url()
        if url is not None:
            self.writer.start('a', attrib={'xlink:href': url})
        if mpl.rcParams['svg.image_inline']:
            buf = BytesIO()
            Image.fromarray(im).save(buf, format="png")
            oid = oid or self._make_id('image', buf.getvalue())
            attrib['xlink:href'] = (
                "data:image/png;base64,\n" +
                base64.b64encode(buf.getvalue()).decode('ascii'))
        else:
            if self.basename is None:
                raise ValueError("Cannot save image data to filesystem when "
                                 "writing SVG to an in-memory buffer")
            filename = '{}.image{}.png'.format(
                self.basename, next(self._image_counter))
            _log.info('Writing image file for inclusion: %s', filename)
            Image.fromarray(im).save(filename)
            oid = oid or 'Im_' + self._make_id('image', filename)
            attrib['xlink:href'] = filename

        attrib['id'] = oid

        if transform is None:
            w = 72.0 * w / self.image_dpi
            h = 72.0 * h / self.image_dpi

            self.writer.element(
                'image',
                transform=generate_transform([
                    ('scale', (1, -1)), ('translate', (0, -h))]),
                x=short_float_fmt(x),
                y=short_float_fmt(-(self.height - y - h)),
                width=short_float_fmt(w), height=short_float_fmt(h),
                attrib=attrib)
        else:
            alpha = gc.get_alpha()
            if alpha != 1.0:
                attrib['opacity'] = short_float_fmt(alpha)

            flipped = (
                Affine2D().scale(1.0 / w, 1.0 / h) +
                transform +
                Affine2D()
                .translate(x, y)
                .scale(1.0, -1.0)
                .translate(0.0, self.height))

            attrib['transform'] = generate_transform(
                [('matrix', flipped.frozen())])
            attrib['style'] = (
                'image-rendering:crisp-edges;'
                'image-rendering:pixelated')
            self.writer.element(
                'image',
                width=short_float_fmt(w), height=short_float_fmt(h),
                attrib=attrib)

        if url is not None:
            self.writer.end('a')
        if clipid is not None:
            self.writer.end('g')
