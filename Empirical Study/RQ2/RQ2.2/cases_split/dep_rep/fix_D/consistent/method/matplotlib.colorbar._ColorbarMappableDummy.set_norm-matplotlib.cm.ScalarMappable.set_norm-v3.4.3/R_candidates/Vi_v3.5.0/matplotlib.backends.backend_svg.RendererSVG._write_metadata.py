    def _write_metadata(self, metadata):
        # Add metadata following the Dublin Core Metadata Initiative, and the
        # Creative Commons Rights Expression Language. This is mainly for
        # compatibility with Inkscape.
        if metadata is None:
            metadata = {}
        metadata = {
            'Format': 'image/svg+xml',
            'Type': 'http://purl.org/dc/dcmitype/StillImage',
            'Creator':
                f'Matplotlib v{mpl.__version__}, https://matplotlib.org/',
            **metadata
        }
        writer = self.writer

        if 'Title' in metadata:
            writer.element('title', text=metadata['Title'])

        # Special handling.
        date = metadata.get('Date', None)
        if date is not None:
            if isinstance(date, str):
                dates = [date]
            elif isinstance(date, (datetime.datetime, datetime.date)):
                dates = [date.isoformat()]
            elif np.iterable(date):
                dates = []
                for d in date:
                    if isinstance(d, str):
                        dates.append(d)
                    elif isinstance(d, (datetime.datetime, datetime.date)):
                        dates.append(d.isoformat())
                    else:
                        raise ValueError(
                            'Invalid type for Date metadata. '
                            'Expected iterable of str, date, or datetime, '
                            'not {!r}.'.format(type(d)))
            else:
                raise ValueError('Invalid type for Date metadata. '
                                 'Expected str, date, datetime, or iterable '
                                 'of the same, not {!r}.'.format(type(date)))
            metadata['Date'] = '/'.join(dates)
        elif 'Date' not in metadata:
            # Do not add `Date` if the user explicitly set `Date` to `None`
            # Get source date from SOURCE_DATE_EPOCH, if set.
            # See https://reproducible-builds.org/specs/source-date-epoch/
            date = os.getenv("SOURCE_DATE_EPOCH")
            if date:
                date = datetime.datetime.utcfromtimestamp(int(date))
                metadata['Date'] = date.replace(tzinfo=UTC).isoformat()
            else:
                metadata['Date'] = datetime.datetime.today().isoformat()

        mid = None
        def ensure_metadata(mid):
            if mid is not None:
                return mid
            mid = writer.start('metadata')
            writer.start('rdf:RDF', attrib={
                'xmlns:dc': "http://purl.org/dc/elements/1.1/",
                'xmlns:cc': "http://creativecommons.org/ns#",
                'xmlns:rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            })
            writer.start('cc:Work')
            return mid

        uri = metadata.pop('Type', None)
        if uri is not None:
            mid = ensure_metadata(mid)
            writer.element('dc:type', attrib={'rdf:resource': uri})

        # Single value only.
        for key in ['title', 'coverage', 'date', 'description', 'format',
                    'identifier', 'language', 'relation', 'source']:
            info = metadata.pop(key.title(), None)
            if info is not None:
                mid = ensure_metadata(mid)
                writer.element(f'dc:{key}', text=info)

        # Multiple Agent values.
        for key in ['creator', 'contributor', 'publisher', 'rights']:
            agents = metadata.pop(key.title(), None)
            if agents is None:
                continue

            if isinstance(agents, str):
                agents = [agents]

            mid = ensure_metadata(mid)
            writer.start(f'dc:{key}')
            for agent in agents:
                writer.start('cc:Agent')
                writer.element('dc:title', text=agent)
                writer.end('cc:Agent')
            writer.end(f'dc:{key}')

        # Multiple values.
        keywords = metadata.pop('Keywords', None)
        if keywords is not None:
            if isinstance(keywords, str):
                keywords = [keywords]

            mid = ensure_metadata(mid)
            writer.start('dc:subject')
            writer.start('rdf:Bag')
            for keyword in keywords:
                writer.element('rdf:li', text=keyword)
            writer.end('rdf:Bag')
            writer.end('dc:subject')

        if mid is not None:
            writer.close(mid)

        if metadata:
            raise ValueError('Unknown metadata key(s) passed to SVG writer: ' +
                             ','.join(metadata))
