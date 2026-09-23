    async def _handle(self, request):
        filename = request.match_info['filename']
        try:
            filepath = self._directory.joinpath(filename).resolve()
            if not self._follow_symlinks:
                filepath.relative_to(self._directory)
        except (ValueError, FileNotFoundError) as error:
            # relatively safe
            raise HTTPNotFound() from error
        except Exception as error:
            # perm error or other kind!
            request.app.logger.exception(error)
            raise HTTPNotFound() from error

        # on opening a dir, load it's contents if allowed
        if filepath.is_dir():
            if self._show_index:
                try:
                    ret = Response(text=self._directory_as_html(filepath),
                                   content_type="text/html")
                except PermissionError:
                    raise HTTPForbidden()
            else:
                raise HTTPForbidden()
        elif filepath.is_file():
            ret = FileResponse(filepath, chunk_size=self._chunk_size)
        else:
            raise HTTPNotFound

        return ret
