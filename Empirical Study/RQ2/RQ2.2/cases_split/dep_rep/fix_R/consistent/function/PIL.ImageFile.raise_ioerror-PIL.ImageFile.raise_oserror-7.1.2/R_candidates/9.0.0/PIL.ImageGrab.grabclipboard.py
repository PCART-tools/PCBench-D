def grabclipboard():
    if sys.platform == "darwin":
        fh, filepath = tempfile.mkstemp(".jpg")
        os.close(fh)
        commands = [
            'set theFile to (open for access POSIX file "'
            + filepath
            + '" with write permission)',
            "try",
            "    write (the clipboard as JPEG picture) to theFile",
            "end try",
            "close access theFile",
        ]
        script = ["osascript"]
        for command in commands:
            script += ["-e", command]
        subprocess.call(script)

        im = None
        if os.stat(filepath).st_size != 0:
            im = Image.open(filepath)
            im.load()
        os.unlink(filepath)
        return im
    elif sys.platform == "win32":
        fmt, data = Image.core.grabclipboard_win32()
        if fmt == "file":  # CF_HDROP
            import struct

            o = struct.unpack_from("I", data)[0]
            if data[16] != 0:
                files = data[o:].decode("utf-16le").split("\0")
            else:
                files = data[o:].decode("mbcs").split("\0")
            return files[: files.index("")]
        if isinstance(data, bytes):
            import io

            data = io.BytesIO(data)
            if fmt == "png":
                from . import PngImagePlugin

                return PngImagePlugin.PngImageFile(data)
            elif fmt == "DIB":
                from . import BmpImagePlugin

                return BmpImagePlugin.DibImageFile(data)
        return None
    else:
        raise NotImplementedError("ImageGrab.grabclipboard() is macOS and Windows only")
