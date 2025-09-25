from __future__ import annotations

from typing import Iterable

from dash import dcc, html

import app as app_module


def _iter_components(component) -> Iterable:
    # Yield component and traverse children recursively
    if isinstance(component, (list, tuple)):
        for child in component:
            yield from _iter_components(child)
        return

    yield component

    children = getattr(component, "children", None)
    if children is None:
        return
    if isinstance(children, (list, tuple)):
        for child in children:
            yield from _iter_components(child)
    else:
        yield from _iter_components(children)


def test_header_present():
    layout = app_module.app.layout
    headers = [
        comp
        for comp in _iter_components(layout)
        if isinstance(comp, html.H1)
    ]
    assert any(getattr(h, "children", None) == "Pink Morsel Sales Visualiser" for h in headers)


def test_graph_present():
    layout = app_module.app.layout
    graphs = [
        comp
        for comp in _iter_components(layout)
        if isinstance(comp, dcc.Graph)
    ]
    assert any(getattr(g, "id", None) == "sales-line-chart" for g in graphs)


def test_region_picker_present():
    layout = app_module.app.layout
    radios = [
        comp
        for comp in _iter_components(layout)
        if isinstance(comp, dcc.RadioItems)
    ]
    assert any(getattr(r, "id", None) == "region-radio" for r in radios)


