def test_polygon_selector_redraw():
    verts = [(50, 50), (150, 50), (50, 150)]
    event_sequence = (polygon_place_vertex(*verts[0]) +
                      polygon_place_vertex(*verts[1]) +
                      polygon_place_vertex(*verts[2]) +
                      polygon_place_vertex(*verts[0]) +
                      # Polygon completed, now remove first two verts
                      polygon_remove_vertex(*verts[1]) +
                      polygon_remove_vertex(*verts[2]) +
                      # At this point the tool should be reset so we can add
                      # more vertices
                      polygon_place_vertex(*verts[1]))

    ax = get_ax()

    def onselect(vertices):
        pass

    tool = widgets.PolygonSelector(ax, onselect)
    for (etype, event_args) in event_sequence:
        do_event(tool, etype, **event_args)
    # After removing two verts, only one remains, and the
    # selector should be automatically resete
    assert tool.verts == verts[0:2]
