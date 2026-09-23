        def __call__(self, path, mutation_size, linewidth,
                     aspect_ratio=1.):
            """
            The __call__ method is a thin wrapper around the transmute method
            and takes care of the aspect ratio.
            """

            path = make_path_regular(path)

            if aspect_ratio is not None:
                # Squeeze the given height by the aspect_ratio

                vertices, codes = path.vertices[:], path.codes[:]
                # Squeeze the height
                vertices[:, 1] = vertices[:, 1] / aspect_ratio
                path_shrunk = Path(vertices, codes)
                # call transmute method with squeezed height.
                path_mutated, fillable = self.transmute(path_shrunk,
                                                        linewidth,
                                                        mutation_size)
                if cbook.iterable(fillable):
                    path_list = []
                    for p in zip(path_mutated):
                        v, c = p.vertices, p.codes
                        # Restore the height
                        v[:, 1] = v[:, 1] * aspect_ratio
                        path_list.append(Path(v, c))
                    return path_list, fillable
                else:
                    return path_mutated, fillable
            else:
                return self.transmute(path, mutation_size, linewidth)
