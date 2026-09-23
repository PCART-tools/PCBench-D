    def save(self, filename, writer=None, fps=None, dpi=None, codec=None,
             bitrate=None, extra_args=None, metadata=None, extra_anim=None,
             savefig_kwargs=None):
        '''Saves a movie file by drawing every frame.

        Parameters
        ----------

        filename : str
            The output filename, e.g., :file:`mymovie.mp4`.

        writer : :class:`MovieWriter` or str, optional
            A `MovieWriter` instance to use or a key that identifies a
            class to use, such as 'ffmpeg'. If ``None``, defaults to
            :rc:`animation.writer`.

        fps : number, optional
           Frames per second in the movie. Defaults to ``None``, which will use
           the animation's specified interval to set the frames per second.

        dpi : number, optional
           Controls the dots per inch for the movie frames.  This combined with
           the figure's size in inches controls the size of the movie.  If
           ``None``, defaults to :rc:`savefig.dpi`.

        codec : str, optional
           The video codec to be used. Not all codecs are supported
           by a given :class:`MovieWriter`. If ``None``, default to
           :rc:`animation.codec`.

        bitrate : number, optional
           Specifies the number of bits used per second in the compressed
           movie, in kilobits per second. A higher number means a higher
           quality movie, but at the cost of increased file size. If ``None``,
           defaults to :rc:`animation.bitrate`.

        extra_args : list, optional
           List of extra string arguments to be passed to the underlying movie
           utility. If ``None``, defaults to :rc:`animation.extra_args`.

        metadata : Dict[str, str], optional
           Dictionary of keys and values for metadata to include in
           the output file. Some keys that may be of use include:
           title, artist, genre, subject, copyright, srcform, comment.

        extra_anim : list, optional
           Additional `Animation` objects that should be included
           in the saved movie file. These need to be from the same
           `matplotlib.figure.Figure` instance. Also, animation frames will
           just be simply combined, so there should be a 1:1 correspondence
           between the frames from the different animations.

        savefig_kwargs : dict, optional
           Is a dictionary containing keyword arguments to be passed
           on to the `savefig` command which is called repeatedly to
           save the individual frames.

        Notes
        -----
        fps, codec, bitrate, extra_args, metadata are used to
        construct a :class:`MovieWriter` instance and can only be
        passed if `writer` is a string.  If they are passed as
        non-`None` and ``writer`` is a :class:`MovieWriter`, a
        `RuntimeError` will be raised.

        '''
        # If the writer is None, use the rc param to find the name of the one
        # to use
        if writer is None:
            writer = rcParams['animation.writer']
        elif (not isinstance(writer, str) and
              any(arg is not None
                  for arg in (fps, codec, bitrate, extra_args, metadata))):
            raise RuntimeError('Passing in values for arguments '
                               'fps, codec, bitrate, extra_args, or metadata '
                               'is not supported when writer is an existing '
                               'MovieWriter instance. These should instead be '
                               'passed as arguments when creating the '
                               'MovieWriter instance.')

        if savefig_kwargs is None:
            savefig_kwargs = {}

        # Need to disconnect the first draw callback, since we'll be doing
        # draws. Otherwise, we'll end up starting the animation.
        if self._first_draw_id is not None:
            self._fig.canvas.mpl_disconnect(self._first_draw_id)
            reconnect_first_draw = True
        else:
            reconnect_first_draw = False

        if fps is None and hasattr(self, '_interval'):
            # Convert interval in ms to frames per second
            fps = 1000. / self._interval

        # Re-use the savefig DPI for ours if none is given
        if dpi is None:
            dpi = rcParams['savefig.dpi']
        if dpi == 'figure':
            dpi = self._fig.dpi

        if codec is None:
            codec = rcParams['animation.codec']

        if bitrate is None:
            bitrate = rcParams['animation.bitrate']

        all_anim = [self]
        if extra_anim is not None:
            all_anim.extend(anim
                            for anim
                            in extra_anim if anim._fig is self._fig)

        # If we have the name of a writer, instantiate an instance of the
        # registered class.
        if isinstance(writer, str):
            if writer in writers.avail:
                writer = writers[writer](fps, codec, bitrate,
                                         extra_args=extra_args,
                                         metadata=metadata)
            else:
                _log.warning("MovieWriter {} unavailable. Trying to use {} "
                             "instead.".format(writer, writers.list()[0]))

                try:
                    writer = writers[writers.list()[0]](fps, codec, bitrate,
                                                        extra_args=extra_args,
                                                        metadata=metadata)
                except IndexError:
                    raise ValueError("Cannot save animation: no writers are "
                                     "available. Please install ffmpeg to "
                                     "save animations.")
        _log.info('Animation.save using %s', type(writer))

        if 'bbox_inches' in savefig_kwargs:
            _log.warning("Warning: discarding the 'bbox_inches' argument in "
                         "'savefig_kwargs' as it may cause frame size "
                         "to vary, which is inappropriate for animation.")
            savefig_kwargs.pop('bbox_inches')

        # Create a new sequence of frames for saved data. This is different
        # from new_frame_seq() to give the ability to save 'live' generated
        # frame information to be saved later.
        # TODO: Right now, after closing the figure, saving a movie won't work
        # since GUI widgets are gone. Either need to remove extra code to
        # allow for this non-existent use case or find a way to make it work.
        with rc_context():
            if rcParams['savefig.bbox'] == 'tight':
                _log.info("Disabling savefig.bbox = 'tight', as it may cause "
                          "frame size to vary, which is inappropriate for "
                          "animation.")
                rcParams['savefig.bbox'] = None
            with writer.saving(self._fig, filename, dpi):
                for anim in all_anim:
                    # Clear the initial frame
                    anim._init_draw()
                for data in zip(*[a.new_saved_frame_seq() for a in all_anim]):
                    for anim, d in zip(all_anim, data):
                        # TODO: See if turning off blit is really necessary
                        anim._draw_next_frame(d, blit=False)
                    writer.grab_frame(**savefig_kwargs)

        # Reconnect signal for first draw if necessary
        if reconnect_first_draw:
            self._first_draw_id = self._fig.canvas.mpl_connect('draw_event',
                                                               self._start)
