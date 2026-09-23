def _write_multiple_frames(im, fp, chunk, rawmode):
    default_image = im.encoderinfo.get("default_image", im.info.get("default_image"))
    duration = im.encoderinfo.get("duration", im.info.get("duration", 0))
    loop = im.encoderinfo.get("loop", im.info.get("loop", 0))
    disposal = im.encoderinfo.get(
        "disposal", im.info.get("disposal", APNG_DISPOSE_OP_NONE)
    )
    blend = im.encoderinfo.get("blend", im.info.get("blend", APNG_BLEND_OP_SOURCE))

    if default_image:
        chain = itertools.chain(im.encoderinfo.get("append_images", []))
    else:
        chain = itertools.chain([im], im.encoderinfo.get("append_images", []))

    im_frames = []
    frame_count = 0
    for im_seq in chain:
        for im_frame in ImageSequence.Iterator(im_seq):
            im_frame = im_frame.copy()
            if im_frame.mode != im.mode:
                if im.mode == "P":
                    im_frame = im_frame.convert(im.mode, palette=im.palette)
                else:
                    im_frame = im_frame.convert(im.mode)
            encoderinfo = im.encoderinfo.copy()
            if isinstance(duration, (list, tuple)):
                encoderinfo["duration"] = duration[frame_count]
            if isinstance(disposal, (list, tuple)):
                encoderinfo["disposal"] = disposal[frame_count]
            if isinstance(blend, (list, tuple)):
                encoderinfo["blend"] = blend[frame_count]
            frame_count += 1

            if im_frames:
                previous = im_frames[-1]
                prev_disposal = previous["encoderinfo"].get("disposal")
                prev_blend = previous["encoderinfo"].get("blend")
                if prev_disposal == APNG_DISPOSE_OP_PREVIOUS and len(im_frames) < 2:
                    prev_disposal = APNG_DISPOSE_OP_BACKGROUND

                if prev_disposal == APNG_DISPOSE_OP_BACKGROUND:
                    base_im = previous["im"]
                    dispose = Image.core.fill("RGBA", im.size, (0, 0, 0, 0))
                    bbox = previous["bbox"]
                    if bbox:
                        dispose = dispose.crop(bbox)
                    else:
                        bbox = (0, 0) + im.size
                    base_im.paste(dispose, bbox)
                elif prev_disposal == APNG_DISPOSE_OP_PREVIOUS:
                    base_im = im_frames[-2]["im"]
                else:
                    base_im = previous["im"]
                delta = ImageChops.subtract_modulo(
                    im_frame.convert("RGB"), base_im.convert("RGB")
                )
                bbox = delta.getbbox()
                if (
                    not bbox
                    and prev_disposal == encoderinfo.get("disposal")
                    and prev_blend == encoderinfo.get("blend")
                ):
                    if isinstance(duration, (list, tuple)):
                        previous["encoderinfo"]["duration"] += encoderinfo["duration"]
                    continue
            else:
                bbox = None
            im_frames.append({"im": im_frame, "bbox": bbox, "encoderinfo": encoderinfo})

    # animation control
    chunk(
        fp,
        b"acTL",
        o32(len(im_frames)),  # 0: num_frames
        o32(loop),  # 4: num_plays
    )

    # default image IDAT (if it exists)
    if default_image:
        ImageFile._save(im, _idat(fp, chunk), [("zip", (0, 0) + im.size, 0, rawmode)])

    seq_num = 0
    for frame, frame_data in enumerate(im_frames):
        im_frame = frame_data["im"]
        if not frame_data["bbox"]:
            bbox = (0, 0) + im_frame.size
        else:
            bbox = frame_data["bbox"]
            im_frame = im_frame.crop(bbox)
        size = im_frame.size
        encoderinfo = frame_data["encoderinfo"]
        frame_duration = int(round(encoderinfo.get("duration", duration)))
        frame_disposal = encoderinfo.get("disposal", disposal)
        frame_blend = encoderinfo.get("blend", blend)
        # frame control
        chunk(
            fp,
            b"fcTL",
            o32(seq_num),  # sequence_number
            o32(size[0]),  # width
            o32(size[1]),  # height
            o32(bbox[0]),  # x_offset
            o32(bbox[1]),  # y_offset
            o16(frame_duration),  # delay_numerator
            o16(1000),  # delay_denominator
            o8(frame_disposal),  # dispose_op
            o8(frame_blend),  # blend_op
        )
        seq_num += 1
        # frame data
        if frame == 0 and not default_image:
            # first frame must be in IDAT chunks for backwards compatibility
            ImageFile._save(
                im_frame,
                _idat(fp, chunk),
                [("zip", (0, 0) + im_frame.size, 0, rawmode)],
            )
        else:
            fdat_chunks = _fdat(fp, chunk, seq_num)
            ImageFile._save(
                im_frame,
                fdat_chunks,
                [("zip", (0, 0) + im_frame.size, 0, rawmode)],
            )
            seq_num = fdat_chunks.seq_num
