    def _get_clip_path(self, clippath, clippath_transform):
        key = (clippath, id(clippath_transform))
        pid = self._clip_paths.get(key)
        if pid is None:
            pid = 'c%x' % len(self._clip_paths)
            clippath_bytes = self._convert_path(
                clippath, clippath_transform, simplify=False)
            self._pswriter.write(f"""\
/{pid} {{
{clippath_bytes}
clip
newpath
}} bind def
""")
            self._clip_paths[key] = pid
        return pid
