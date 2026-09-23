    @docstring.dedent_interpd
    def __init__(self,
                 numsides,
                 rotation=0,
                 sizes=(1,),
                 **kwargs):
        """
        *numsides*
            the number of sides of the polygon

        *rotation*
            the rotation of the polygon in radians

        *sizes*
            gives the area of the circle circumscribing the
            regular polygon in points^2

        %(Collection)s

        Example: see :doc:`/gallery/event_handling/lasso_demo` for a
        complete example::

            offsets = np.random.rand(20,2)
            facecolors = [cm.jet(x) for x in np.random.rand(20)]
            black = (0,0,0,1)

            collection = RegularPolyCollection(
                numsides=5, # a pentagon
                rotation=0, sizes=(50,),
                facecolors=facecolors,
                edgecolors=(black,),
                linewidths=(1,),
                offsets=offsets,
                transOffset=ax.transData,
                )
        """
        Collection.__init__(self, **kwargs)
        self.set_sizes(sizes)
        self._numsides = numsides
        self._paths = [self._path_generator(numsides)]
        self._rotation = rotation
        self.set_transform(transforms.IdentityTransform())
