    @_api.deprecated("3.8")
    @property
    def collections(self):
        # On access, make oneself invisible and instead add the old-style collections
        # (one PathCollection per level).  We do not try to further split contours into
        # connected components as we already lost track of what pairs of contours need
        # to be considered as single units to draw filled regions with holes.
        if not hasattr(self, "_old_style_split_collections"):
            self.set_visible(False)
            fcs = self.get_facecolor()
            ecs = self.get_edgecolor()
            lws = self.get_linewidth()
            lss = self.get_linestyle()
            self._old_style_split_collections = []
            for idx, path in enumerate(self._paths):
                pc = mcoll.PathCollection(
                    [path] if len(path.vertices) else [],
                    alpha=self.get_alpha(),
                    antialiaseds=self._antialiaseds[idx % len(self._antialiaseds)],
                    transform=self.get_transform(),
                    zorder=self.get_zorder(),
                    label="_nolegend_",
                    facecolor=fcs[idx] if len(fcs) else "none",
                    edgecolor=ecs[idx] if len(ecs) else "none",
                    linewidths=[lws[idx % len(lws)]],
                    linestyles=[lss[idx % len(lss)]],
                )
                if self.filled:
                    pc.set(hatch=self.hatches[idx % len(self.hatches)])
                self._old_style_split_collections.append(pc)
            for col in self._old_style_split_collections:
                self.axes.add_collection(col)
        return self._old_style_split_collections
