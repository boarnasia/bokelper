"""Figure with additional graph methods"""

from bokeh.models import HoverTool
from bokeh.models.sources import ColumnDataSource
from bokeh.plotting.figure import Figure
from bokeh.models.renderers import GlyphRenderer

import numpy as np
import pandas as pd


class FigureEx(Figure):
    """Figure class extended

    This has some plotting methods.

    - bbands: plots bollinger bands chat
    - candle: plots candle stick chart
    - hist: plots histgram chart
    """
    __subtype__ = "FigureEx"
    __view_model__ = "Plot"

    def bbands(self, srs: pd.Series, window: int = 20,
               auto_tooltip: bool = True) -> dict:
        """plots bollinger bands chart"""
        std = srs.rolling(window).std()
        m = srs.rolling(window).mean()
        u1, l1 = m + std, m - std
        u2, l2 = m + (std * 2), m - (std * 2)
        u3, l3 = m + (std * 3), m - (std * 3)

        c1, c2, c3, cm = ('#2ca02c', '#ff7f0e', '#1f77b4', '#d62728')

        data = dict(
            index     = srs.index,
            bbands_u1 = u1,
            bbands_u2 = u2,
            bbands_u3 = u3,
            bbands_l1 = l1,
            bbands_l2 = l2,
            bbands_l3 = l3,
            bbands_m  = m,
        )
        source = ColumnDataSource(data=data)

        kwargs = dict(
            source=source,
            name='bbands',
            muted_alpha=0.2,
        )

        self.line('index', 'bbands_u3',
                  color=c3, muted_color=c3,
                  legend='BBAND σ3', **kwargs)
        self.line('index', 'bbands_l3',
                  color=c3, muted_color=c3,
                  legend='BBAND σ3', **kwargs)
        self.line('index', 'bbands_u2',
                  color=c2, muted_color=c2,
                  legend='BBAND σ2', **kwargs)
        self.line('index', 'bbands_l2',
                  color=c2, muted_color=c2,
                  legend='BBAND σ2', **kwargs)
        self.line('index', 'bbands_u1',
                  color=c1, muted_color=c1,
                  legend='BBAND σ1', **kwargs)
        self.line('index', 'bbands_l1',
                  color=c1, muted_color=c1,
                  legend='BBAND σ1', **kwargs)
        self.line('index', 'bbands_m',
                  color=cm, muted_color=cm,
                  legend='BBAND', **kwargs)

        if auto_tooltip:
            self.add_tools(HoverTool(
                names=['bbands'],
                tooltips=[
                    ('日付', '@index{%Y-%m-%d}'),
                    ('BB σ3', '@bbands_u3{,}'),
                    ('BB Middle', '@bbands_m{,}'),
                    ('BB -σ3', '@bbands_l3{,}'),
                ],
                formatters={'index': 'datetime'}
            ))

        return data

    def candle(self, df: pd.DataFrame, auto_tooltip: bool = True) -> None:
        """plots candle stick chart"""

        inc = df.close >= df.open
        dec = df.open > df.close
        w   = 12 * 60 * 60 * 1000  # half day in ms

        source_inc = ColumnDataSource(data=dict(
            index = df.index[inc],
            candle_open = df.open[inc],
            candle_close = df.close[inc],
            candle_high = df.high[inc],
            candle_low = df.low[inc],
        ))
        source_dec = ColumnDataSource(data=dict(
            index = df.index[dec],
            candle_open = df.open[dec],
            candle_close = df.close[dec],
            candle_high = df.high[dec],
            candle_low = df.low[dec],
        ))

        self.segment('index', 'candle_high', 'index', 'candle_low',
                     source=source_inc, color='black', name='candle')
        self.segment('index', 'candle_high', 'index', 'candle_low',
                     source=source_dec, color='red', name='candle')
        self.vbar('index', w, 'candle_open', 'candle_close',
                  source=source_inc, fill_color="#D5E1DD",
                  line_color="black", name='candle')
        self.vbar('index', w, 'candle_open', 'candle_close',
                  source=source_inc, fill_color="#F2583E",
                  line_color="red", name='candle')

        if auto_tooltip:
            self.add_tools(HoverTool(
                names=['candle'],
                tooltips=[
                    ('日付', '@index{%Y-%m-%d}'),
                    ('始値', '@candle_open{,.2f}'),
                    ('終値', '@candle_close{,.2f}'),
                    ('高値', '@candle_high{,.2f}'),
                    ('安値', '@candle_low{,.2f}'),
                ],
                formatters={'index': 'datetime'}
            ))

    def hist(self, srs: pd.Series, bins: int = 10,
             auto_tooltip: bool = True) -> dict:
        """plots histgram chart"""

        # 分布の計算
        y, x_buf = np.histogram(srs, bins=bins)

        # x を中間点に微調整。また x ラベルを作成。
        x, x_from, x_to = [], [], []
        for idx in range(len(x_buf) - 1):
            x.append((x_buf[idx] + x_buf[idx + 1]) / 2)
            x_from.append(x_buf[idx])
            x_to.append(x_buf[idx + 1])

        # データソースに格納
        data = dict(
            hist_x = x,
            hist_y = y,
            hist_x_from=x_from,
            hist_x_to=x_to,
        )
        source = ColumnDataSource(data=data)

        # 縦棒の幅を決定。少し細めにしてバーがかぶらないようにしています。
        width = srs.max() / (bins * 1.4)

        self.vbar(x='hist_x', width=width, top='hist_y',
                  source=source, name='hist')

        # 指定があればツールチップを追加
        if auto_tooltip:
            self.add_tools(HoverTool(
                names=['hist'],
                tooltips=[
                    ('x', '@hist_x{,.2f}'),
                    ('y', '@hist_y{,}'),
                    ('range', '@hist_x_from{,.2f} - @hist_x_from{,.2f}'),
                ],
            ))

        return data

    def grayscale(self, img: np.ndarray, bits: int) -> GlyphRenderer:
        """plots grayscale image

        Example:

            >>> import bokelper as bkh
            >>> from sklearn import datasets
            >>> bkh.output_notebook()
            >>>
            >>> digits = datasets.load_digits()
            >>> fig = bkh.figure(
            ...     plot_width=100, plot_height=150,
            ...     toolbar_location=None,
            ...     tooltips=[("x", "$x"), ("y", "$y"), ("value", "@image")])
            >>> fig.grayscale(digits['data'][0].reshape(8, 8), 4)
            >>> bkh.show(fig)

        Args:
            img: numpy.ndarray
                ndarray which has int columns in 2 dimentions.

            bits: int
                bit length of grayscale image

        Return: GlyphRenderer
        """
        img = img.copy().astype('uint8')
        w, h = img.shape
        img_rgba = np.empty((w, h), dtype=np.uint32)
        view = img_rgba.view(dtype=np.uint8).reshape((w, h, 4))
        for i in range(w):
            for j in range(h):
                col = int(255 - ((img[i, j] / 15) * 255))
                view[i, j, 0:3] = col
        view[:, :, 3] = 255
        img_rgba = np.flipud(img_rgba)

        return self.image_rgba(image=[img_rgba], x=0, y=0, dw=w, dh=h)


def figure(**kwargs):
    fig = FigureEx(**kwargs)
    return fig
figure.__doc__ = Figure.__doc__  # noqa
