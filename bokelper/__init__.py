from typing import Iterable

from bokeh.io import output_notebook, show
from bokeh.models import HoverTool, Range1d, LinearAxis, RangeTool
from bokeh.models.sources import ColumnDataSource
from bokeh.layouts import Column, Row

import bokeh.palettes
import itertools

from .figure import figure

__version__ = '0.1.0'

__all__ = [
    'output_notebook', 'show',
    'HoverTool', 'Range1d', 'LinearAxis', 'RangeTool',
    'ColumnDataSource',
    'Column', 'Row',
    'palette', 'figure',
]


def palette(name: str = 'Category10_10') -> Iterable:
    """Return color palette in cycle iteration

    Example::

      >>> colors = palette()
      >>> next(colors)
      '#1f77b4'
      >>> next(colors)
      '#ff7f0e'
      >>> c1, c2 = next(colors), next(colors)

    Args:
      name: str   Palette name in bokeh.palettes

    Return: itertools.cycle
      A palette list in cycle iteration
    """
    plt = getattr(bokeh.palettes, name)
    return itertools.cycle(plt)


def muted_color(color: str, alpha: float = 0.2):
    """Return dict of color, muted_color and muted_alpha
    from given color.

    Example::

      >>> colors = palette()
      >>> c = next(colors)
      >>> muted_color(c)
      {'color': '#1f77b4', 'muted_color': '#1f77b4', 'muted_alpha': 0.2}

      >>> fig.line(x, y, **muted_color(c))
      >>> fig.legend.click_policy = 'mute'
      >>> show(fig)
    """

    return dict(
        color=color,
        muted_color=color,
        muted_alpha=alpha,
    )
