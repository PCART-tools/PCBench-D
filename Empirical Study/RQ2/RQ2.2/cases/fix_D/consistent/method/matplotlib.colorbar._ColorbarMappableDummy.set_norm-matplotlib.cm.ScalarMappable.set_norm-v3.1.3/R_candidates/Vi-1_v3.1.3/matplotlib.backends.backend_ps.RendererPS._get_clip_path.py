    def _get_clip_path(self, clippath, clippath_transform):
        key = (clippath, id(clippath_transform))
        pid = self._clip_paths.get(key)
        if pid is None:
            pid = 'c%x' % len(self._clip_paths)
            ps_cmd = ['/%s {' % pid]
            ps_cmd.append(self._convert_path(clippath, clippath_transform,
                                             simplify=False))
            ps_cmd.extend(['clip', 'newpath', '} bind def\n'])
            self._pswriter.write('\n'.join(ps_cmd))
            self._clip_paths[key] = pid
        return pid
