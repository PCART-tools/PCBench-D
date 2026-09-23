    def _directory_as_html(self, filepath):
        "returns directory's index as html"
        # sanity check
        assert filepath.is_dir()

        relative_path_to_dir = filepath.relative_to(self._directory).as_posix()
        index_of = "Index of /{}".format(relative_path_to_dir)
        head = "<head>\n<title>{}</title>\n</head>".format(index_of)
        h1 = "<h1>{}</h1>".format(index_of)

        index_list = []
        dir_index = filepath.iterdir()
        for _file in sorted(dir_index):
            # show file url as relative to static path
            rel_path = _file.relative_to(self._directory).as_posix()
            file_url = self._prefix + '/' + rel_path

            # if file is a directory, add '/' to the end of the name
            if _file.is_dir():
                file_name = "{}/".format(_file.name)
            else:
                file_name = _file.name

            index_list.append(
                '<li><a href="{url}">{name}</a></li>'.format(url=file_url,
                                                             name=file_name)
            )
        ul = "<ul>\n{}\n</ul>".format('\n'.join(index_list))
        body = "<body>\n{}\n{}\n</body>".format(h1, ul)

        html = "<html>\n{}\n{}\n</html>".format(head, body)

        return html
