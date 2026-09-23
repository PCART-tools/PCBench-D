def _save(im, fp, filename):
    if im.mode not in ("RGB", "RGBA"):
        raise OSError(f"cannot write mode {im.mode} as DDS")

    fp.write(
        o32(DDS_MAGIC)
        + o32(124)  # header size
        + o32(
            DDSD_CAPS | DDSD_HEIGHT | DDSD_WIDTH | DDSD_PITCH | DDSD_PIXELFORMAT
        )  # flags
        + o32(im.height)
        + o32(im.width)
        + o32((im.width * (32 if im.mode == "RGBA" else 24) + 7) // 8)  # pitch
        + o32(0)  # depth
        + o32(0)  # mipmaps
        + o32(0) * 11  # reserved
        + o32(32)  # pfsize
        + o32(DDS_RGBA if im.mode == "RGBA" else DDPF_RGB)  # pfflags
        + o32(0)  # fourcc
        + o32(32 if im.mode == "RGBA" else 24)  # bitcount
        + o32(0xFF0000)  # rbitmask
        + o32(0xFF00)  # gbitmask
        + o32(0xFF)  # bbitmask
        + o32(0xFF000000 if im.mode == "RGBA" else 0)  # abitmask
        + o32(DDSCAPS_TEXTURE)  # dwCaps
        + o32(0)  # dwCaps2
        + o32(0)  # dwCaps3
        + o32(0)  # dwCaps4
        + o32(0)  # dwReserved2
    )
    if im.mode == "RGBA":
        r, g, b, a = im.split()
        im = Image.merge("RGBA", (a, r, g, b))
    ImageFile._save(im, fp, [("raw", (0, 0) + im.size, 0, (im.mode[::-1], 0, 1))])
