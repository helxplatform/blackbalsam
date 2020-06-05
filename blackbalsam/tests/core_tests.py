import unittest

from pyspark.conf import SparkConf
from pyspark.sql.dataframe import DataFrame

from blackbalsam.core import Blackbalsam


class TestCoreBlackbalsam(unittest.TestCase):

    def setUp(self):
        self.bb = Blackbalsam()
        self.conf = SparkConf().getAll()
        self.spark = self.bb.get_spark({
            "spark.app.name": "pyspark_test_blackbalsam",
            "spark.executor.instances": "2",
            "spark.driver.memory": "512M",
            "spark.executor.memory": "512M",
        })

    def tearDown(self):
        self.spark.stop()
        SparkConf().setAll(self.conf())

    def test_spark_methods(self):
        import pandas as pd
        data_pandas = pd.DataFrame({"make": ["Jaguar", "MG", "MINI", "Rover", "Lotus"],
                                    "registration": ["AB98ABCD", "BC99BCDF", "CD00CDE", "DE01DEF", "EF02EFG"],
                                    "year": [1998, 1999, 2000, 2001, 2002]})
        data = self.spark.createDataFrame(data_pandas)
        self.assertIsInstance(data, DataFrame)
