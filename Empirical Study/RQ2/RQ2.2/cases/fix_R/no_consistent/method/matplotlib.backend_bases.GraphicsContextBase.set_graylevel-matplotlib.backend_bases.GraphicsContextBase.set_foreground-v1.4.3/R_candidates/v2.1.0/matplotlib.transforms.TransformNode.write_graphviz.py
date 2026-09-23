        def write_graphviz(self, fobj, highlight=[]):
            """
            For debugging purposes.

            Writes the transform tree rooted at 'self' to a graphviz "dot"
            format file.  This file can be run through the "dot" utility
            to produce a graph of the transform tree.

            Affine transforms are marked in blue.  Bounding boxes are
            marked in yellow.

            *fobj*: A Python file-like object

            Once the "dot" file has been created, it can be turned into a
            png easily with::

                $> dot -Tpng -o $OUTPUT_FILE $DOT_FILE

            """
            seen = set()

            def recurse(root):
                if root in seen:
                    return
                seen.add(root)
                props = {}
                label = root.__class__.__name__
                if root._invalid:
                    label = '[%s]' % label
                if root in highlight:
                    props['style'] = 'bold'
                props['shape'] = 'box'
                props['label'] = '"%s"' % label
                props = ' '.join(['%s=%s' % (key, val)
                                  for key, val
                                  in six.iteritems(props)])

                fobj.write('%s [%s];\n' %
                           (hash(root), props))

                if hasattr(root, '_children'):
                    for child in root._children:
                        name = '?'
                        for key, val in six.iteritems(root.__dict__):
                            if val is child:
                                name = key
                                break
                        fobj.write('"%s" -> "%s" [label="%s", fontsize=10];\n'
                                    % (hash(root),
                                    hash(child),
                                    name))
                        recurse(child)

            fobj.write("digraph G {\n")
            recurse(self)
            fobj.write("}\n")
