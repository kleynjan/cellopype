## how to run unit tests (bloody ridiculous, this)
# $ cd ../src
# $ python -m unittest discover ../tests

import unittest
import pandas as pd

from cellopype.helpers import deep_eq


class DeepEqTests(unittest.TestCase):
    def test_dfs(self):
        self.df1 = pd.DataFrame([1, 2, 3], columns=["value"])
        self.df2 = pd.DataFrame([1, 2, 3], columns=["value"])
        self.df3 = pd.DataFrame([1, 2, 3, 4], columns=["value"])
        self.assertTrue(deep_eq(self.df1, self.df2))
        self.assertFalse(deep_eq(self.df1, self.df3))
        self.df2.loc[0, "value"] = 9
        self.assertFalse(deep_eq(self.df1, self.df2))
        self.df2.loc[0, "value"] = 1
        self.assertTrue(deep_eq(self.df1, self.df2))
        self.assertFalse(
            deep_eq(
                self.df1, self.df1.rename(columns={"value": "x"}, inplace=True)
            )
        )

    def test_series(self):
        self.s1 = pd.Series([1, 2, 3, 4])
        self.s2 = pd.Series([1, 2, 3, 4])
        self.s3 = pd.Series([1, 2, 3, 9])
        self.assertTrue(deep_eq(self.s1, self.s2))
        self.assertFalse(deep_eq(self.s1, self.s3))
        self.s2.loc[0] = 9
        self.assertFalse(deep_eq(self.s1, self.s2))
        self.s2.loc[0] = 1
        self.assertTrue(deep_eq(self.s1, self.s2))
        self.df1 = pd.DataFrame([1, 2, 3], columns=["value"])
        self.assertFalse(deep_eq(self.s1, self.df1))


if __name__ == "__main__":
    unittest.main()
