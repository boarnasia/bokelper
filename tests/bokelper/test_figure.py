import pytest  # noqa
import numpy as np
import pandas as pd
from sklearn import datasets

import bokelper as bkh


class TestFigureEx:

    def test_bbands(self):
        fig = bkh.figure(plot_width=600, plot_height=300)
        x = np.linspace(1, 11, 100)
        y = np.random.uniform(1, 100, 100) * np.sin(np.linspace(0, 12, 100))
        fig = bkh.figure(plot_width = 800, plot_height = 400)
        fig.bbands(pd.Series(y, index=x))

        # test passed when process didn't make exception
        assert True

    def test_candle(self):
        fig = bkh.figure(plot_width=600, plot_height=300)
        x = np.linspace(1, 11, 100)
        y = np.random.uniform(1, 100, 100) * np.sin(np.linspace(0, 12, 100))
        df = pd.DataFrame(
            dict(
                open=y,
                close=y + 10,
                high=y + 15,
                low=y - 5,
            ),
            index=x,
        )
        fig = bkh.figure(plot_width = 800, plot_height = 400)
        fig.candle(df)

        # test passed when process didn't make exception
        assert True

    def test_hist(self):
        fig = bkh.figure(plot_width=600, plot_height=300)
        x = np.linspace(1, 11, 100)
        y = np.random.uniform(1, 100, 100) * np.sin(np.linspace(0, 12, 100))
        fig = bkh.figure(plot_width = 800, plot_height = 400)
        fig.hist(pd.Series(y, index=x))

        # test passed when process didn't make exception
        assert True

    def test_grayscale(self):
        digits = datasets.load_digits()
        fig = bkh.figure()
        fig.grayscale(digits['data'][0].reshape(8, 8), 4)

        assert True
