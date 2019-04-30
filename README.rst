Bokelper = Bokeh + helper
=========================

It's Bokeh_ helper library.

----------------
Import Shortcuts
----------------

There are some shortcut to avoide annoying import.

Below elements can be imported from bokelper at once.

- from bokeh.io import output_notebook, show, push_notebook
- from bokeh.models import HoverTool, Range1d, LinearAxis, RangeTool
- from bokeh.models.sources import ColumnDataSource
- from bokeh.layouts import Column, Row

Example:

.. code-block:: python

  from bokelper import (
      output_notebook, show, push_notebook,
      HoverTool, Range1d, LinearAxis, RangeTool,
      ColumnDataSource,
      Column, Row,
  )
  
or
  
.. code-block:: python

  from bokelper import *

---------------------
Functions and Methods
---------------------

bokelper.palette(name: str = 'Category10_10')
  returns cycle iterable color palette.
  
bokelper.muted_color(color: str, muted_alpha: float = 0.2)
  returns dict of color, muted_color and muted_alpha from given color.
  
bokelper.figure.FigureEx.bbands(srs: pd.Series, window: int = 20, auto_tooltip: bool = True)
  plots a bollinger bands
  
bokelper.figure.FigureEx.candle(df: pd.DataFrame, auto_tooltip: bool = True)
  plots a candle stick chart
  
bokelper.figure.FigureEx.hist(srs: pd.Series, bins: int = 10, auto_tooltip: bool = True)
  plots a histgram chart

bokelper.figure.FigureEx.grayscale(self, img: np.ndarray, bits: int)
  plots a grayscale image

.. _Bokeh: https://bokeh.pydata.org/
