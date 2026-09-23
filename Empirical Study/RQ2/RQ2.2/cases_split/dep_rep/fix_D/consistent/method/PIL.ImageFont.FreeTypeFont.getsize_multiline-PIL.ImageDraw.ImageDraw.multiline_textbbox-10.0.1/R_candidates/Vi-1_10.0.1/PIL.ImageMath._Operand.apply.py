    def apply(self, op, im1, im2=None, mode=None):
        im1 = self.__fixup(im1)
        if im2 is None:
            # unary operation
            out = Image.new(mode or im1.mode, im1.size, None)
            im1.load()
            try:
                op = getattr(_imagingmath, op + "_" + im1.mode)
            except AttributeError as e:
                msg = f"bad operand type for '{op}'"
                raise TypeError(msg) from e
            _imagingmath.unop(op, out.im.id, im1.im.id)
        else:
            # binary operation
            im2 = self.__fixup(im2)
            if im1.mode != im2.mode:
                # convert both arguments to floating point
                if im1.mode != "F":
                    im1 = im1.convert("F")
                if im2.mode != "F":
                    im2 = im2.convert("F")
            if im1.size != im2.size:
                # crop both arguments to a common size
                size = (min(im1.size[0], im2.size[0]), min(im1.size[1], im2.size[1]))
                if im1.size != size:
                    im1 = im1.crop((0, 0) + size)
                if im2.size != size:
                    im2 = im2.crop((0, 0) + size)
            out = Image.new(mode or im1.mode, im1.size, None)
            im1.load()
            im2.load()
            try:
                op = getattr(_imagingmath, op + "_" + im1.mode)
            except AttributeError as e:
                msg = f"bad operand type for '{op}'"
                raise TypeError(msg) from e
            _imagingmath.binop(op, out.im.id, im1.im.id, im2.im.id)
        return _Operand(out)
