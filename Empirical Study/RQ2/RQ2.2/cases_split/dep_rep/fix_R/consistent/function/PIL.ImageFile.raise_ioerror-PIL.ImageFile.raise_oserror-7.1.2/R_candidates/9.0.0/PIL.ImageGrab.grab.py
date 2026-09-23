def grab(bbox=None, include_layered_windows=False, all_screens=False, xdisplay=None):
    if xdisplay is None:
        if sys.platform == "darwin":
            fh, filepath = tempfile.mkstemp(".png")
            os.close(fh)
            subprocess.call(["screencapture", "-x", filepath])
            im = Image.open(filepath)
            im.load()
            os.unlink(filepath)
            if bbox:
                im_cropped = im.crop(bbox)
                im.close()
                return im_cropped
            return im
        elif sys.platform == "win32":
            offset, size, data = Image.core.grabscreen_win32(
                include_layered_windows, all_screens
            )
            im = Image.frombytes(
                "RGB",
                size,
                data,
                # RGB, 32-bit line padding, origin lower left corner
                "raw",
                "BGR",
                (size[0] * 3 + 3) & -4,
                -1,
            )
            if bbox:
                x0, y0 = offset
                left, top, right, bottom = bbox
                im = im.crop((left - x0, top - y0, right - x0, bottom - y0))
            return im
    # use xdisplay=None for default display on non-win32/macOS systems
    if not Image.core.HAVE_XCB:
        raise OSError("Pillow was built without XCB support")
    size, data = Image.core.grabscreen_x11(xdisplay)
    im = Image.frombytes("RGB", size, data, "raw", "BGRX", size[0] * 4, 1)
    if bbox:
        im = im.crop(bbox)
    return im
