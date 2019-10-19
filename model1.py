# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 13:46:40 2019

@author: rmahajan14
"""

from loader1 import load_spark_df, load_pandas_df
import pyspark
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.mllib.evaluation import RegressionMetrics, RankingMetrics


def get_als_model_rmse(df, rank):
    train, test = df.randomSplit([0.9, 0.1], seed=1)
    als = ALS(maxIter=5,
              regParam=0.09,
              rank=rank,
              userCol="userId",
              itemCol="movieId",
              ratingCol="rating",
              coldStartStrategy="drop",
              nonnegative=True)

    model = als.fit(train)
    evaluator = RegressionEvaluator(metricName="rmse",
                                    labelCol="rating",
                                    predictionCol="prediction")
    predictions = model.transform(test)
    rmse = evaluator.evaluate(predictions)
    print(f'RMSE is {rmse}')
    return (predictions, model, rmse)


def get_best_rank(df):
    rmse_dict = {}
    for rank in [1, 2, 4, 8, 16, 32, 64, 128]:
        #    for rank in [64, 128]:
        print(f'Rank is {rank}')
        _, _, rmse = get_als_model_rmse(df, rank)
        rmse_dict[rank] = rmse
    return rmse_dict


def get_rank_report(df):

    rank = 64
    predictions, model, rmse = get_als_model_rmse(df, rank)
    valuesAndPreds = predictions.rdd.map(lambda x: (x.rating, x.prediction))
    regressionmetrics = RegressionMetrics(valuesAndPreds)
    rankingmetrics = RankingMetrics(valuesAndPreds)
    print("MAE = %s" % regressionmetrics.meanAbsoluteError)


if __name__ == '__main__':
    dir_name = 'ml-latest-small'
    ratings_spark_df = load_spark_df(dir_name, 'ratings', use_cache=True)
    #rmse_dict = get_best_rank(ratings_spark_df)
    get_rank_report(ratings_spark_df)
#    print("RMSE=" + str(rmse))
#    predictions.show()
