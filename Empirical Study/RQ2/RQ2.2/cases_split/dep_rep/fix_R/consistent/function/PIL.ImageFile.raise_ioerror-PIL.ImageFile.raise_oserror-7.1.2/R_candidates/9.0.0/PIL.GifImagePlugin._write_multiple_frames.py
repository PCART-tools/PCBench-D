def _write_multiple_frames(im, fp, palette):

    duration = im.encoderinfo.get("duration", im.info.get("duration"))
    disposal = im.encoderinfo.get("disposal", im.info.get("disposal"))

    im_frames = []
    frame_count = 0
    background_im = None
    for imSequence in itertools.chain([im], im.encoderinfo.get("append_images", [])):
        for im_frame in ImageSequence.Iterator(imSequence):
            # a copy is required here since seek can still mutate the image
            im_frame = _normalize_mode(im_frame.copy())
            if frame_count == 0:
                for k, v in im_frame.info.items():
                    im.encoderinfo.setdefault(k, v)
            im_frame = _normalize_palette(im_frame, palette, im.encoderinfo)

            encoderinfo = im.encoderinfo.copy()
            if isinstance(duration, (list, tuple)):
                encoderinfo["duration"] = duration[frame_count]
            if isinstance(disposal, (list, tuple)):
                encoderinfo["disposal"] = disposal[frame_count]
            frame_count += 1

            if im_frames:
                # delta frame
                previous = im_frames[-1]
                if encoderinfo.get("disposal") == 2:
                    if background_im is None:
                        color = im.encoderinfo.get(
                            "transparency", im.info.get("transparency", (0, 0, 0))
                        )
                        background = _get_background(im_frame, color)
                        background_im = Image.new("P", im_frame.size, background)
                        background_im.putpalette(im_frames[0]["im"].palette)
                    base_im = background_im
                else:
                    base_im = previous["im"]
                if _get_palette_bytes(im_frame) == _get_palette_bytes(base_im):
                    delta = ImageChops.subtract_modulo(im_frame, base_im)
                else:
                    delta = ImageChops.subtract_modulo(
                        im_frame.convert("RGB"), base_im.convert("RGB")
                    )
                bbox = delta.getbbox()
                if not bbox:
                    # This frame is identical to the previous frame
                    if duration:
                        previous["encoderinfo"]["duration"] += encoderinfo["duration"]
                    continue
            else:
                bbox = None
            im_frames.append({"im": im_frame, "bbox": bbox, "encoderinfo": encoderinfo})

    if len(im_frames) > 1:
        for frame_data in im_frames:
            im_frame = frame_data["im"]
            if not frame_data["bbox"]:
                # global header
                for s in _get_global_header(im_frame, frame_data["encoderinfo"]):
                    fp.write(s)
                offset = (0, 0)
            else:
                # compress difference
                if not palette:
                    frame_data["encoderinfo"]["include_color_table"] = True

                im_frame = im_frame.crop(frame_data["bbox"])
                offset = frame_data["bbox"][:2]
            _write_frame_data(fp, im_frame, offset, frame_data["encoderinfo"])
        return True
    elif "duration" in im.encoderinfo and isinstance(
        im.encoderinfo["duration"], (list, tuple)
    ):
        # Since multiple frames will not be written, add together the frame durations
        im.encoderinfo["duration"] = sum(im.encoderinfo["duration"])
