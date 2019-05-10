from typing import *   # noqa

import numpy as np

from bokeh.io.notebook import CommsHandle, push_notebook
from bokeh.models.renderers import GlyphRenderer
from keras.callbacks import Callback


class HistoryPlotter(Callback):
    """Plots keras fit history
    Callback class for `fit method of keras model
    <https://keras.io/models/sequential/#fit>`_.
    Every epoch ends, it updates `data_source` property of rendereres,
    then calls push_notebook() of bokeh with given handle.
    `data_sources` could have keys of 'loss', 'accuracy', 'val_loss',
    'val_accuracy', etc, however these keys are not fixed, and are
    determined according to the fit method parameters.
    You can know what keys you can handle by dumping history property of
    history object that the fit method returns.
    Example:
    >>> source = bkh.ColumnDataSource(dict(x=[], loss=[],
    ...                               binary_accuracy=[]))
    >>> fig = bkh.figure(plot_width=600, plot_height=200,
    ...                  toolbar_location=None)
    >>> c = bkh.palette()
    >>> renderers = [
    ...     fig.line(x='x', y='loss', source=source, color=next(c)),
    ...     fig.line(x='x', y='binary_accuracy', source=source,
    ...              color=next(c)),
    ... ]
    >>> handle = bkh.show(fig, notebook_handle=True)
    >>> hist = model.fit(x_train, y_train, epochs=100, batch_size=200,
    ...     validation_split=0.2,
    ...     verbose=0,
    ...     callbacks=[
    ...         UpdateHistoryPlot(handle, renderers),
    ...     ]
    ... )
    """
    def __init__(self, handle: CommsHandle, renderers: List[GlyphRenderer]):
        """Initializing method.
        Args:
            handle: bokeh.io.notebook.CommsHandle
                Handle that bokeh.io.show function returns
            renderers: List[bokeh.models.renderers.GlyphRenderer]
                Renderer list of the plot
        """
        super().__init__()
        self.handle        = handle
        self.renderers     = renderers
        self.history: dict = dict()

    def on_epoch_end(self, epoch: int, logs: dict):
        """Callback method that runs when every epoch ends
        It updates given renderer data_source property.
        See https://keras.io/callbacks/, if you know detail.
        """
        # Records logs to self.history
        for k, v in logs.items():
            if k not in self.history:
                self.history[k] = list()
            self.history[k].append(v)

        # Updates renderers
        for renderer in self.renderers:
            renderer.data_source.data.update(
                x=np.arange(epoch + 1),
                **self.history,
            )

        # Finally, update the plot
        push_notebook(handle=self.handle)