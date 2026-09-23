    def apply(
        self,
        op: str,
        im1: _Operand | float,
        im2: _Operand | float | None = None,
        mode: str | None = None,
    ) -> _Operand:
        im_1 = self.__fixup(im1)
        if im2 is None:
            # unary operation
            out = Image.new(mode or im_1.mode, im_1.size, None)
            im_1.load()
            try:
                op = getattr(_imagingmath, op + "_" + im_1.mode)
            except AttributeError as e:
                msg = f"bad operand type for '{op}'"
                raise TypeError(msg) from e
            _imagingmath.unop(op, out.im.id, im_1.im.id)
        else:
            # binary operation
            im_2 = self.__fixup(im2)
            if im_1.mode != im_2.mode:
                # convert both arguments to floating point
                if im_1.mode != "F":
                    im_1 = im_1.convert("F")
                if im_2.mode != "F":
                    im_2 = im_2.convert("F")
            if im_1.size != im_2.size:
                # crop both arguments to a common size
                size = (
                    min(im_1.size[0], im_2.size[0]),
                    min(im_1.size[1], im_2.size[1]),
                )
                if im_1.size != size:
                    im_1 = im_1.crop((0, 0) + size)
                if im_2.size != size:
                    im_2 = im_2.crop((0, 0) + size)
            out = Image.new(mode or im_1.mode, im_1.size, None)
            im_1.load()
            im_2.load()
            try:
                op = getattr(_imagingmath, op + "_" + im_1.mode)
            except AttributeError as e:
                msg = f"bad operand type for '{op}'"
                raise TypeError(msg) from e
            _imagingmath.binop(op, out.im.id, im_1.im.id, im_2.im.id)
        return _Operand(out)
