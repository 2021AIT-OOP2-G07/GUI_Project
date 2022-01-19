
from pymongo import MongoClient


def P_reg(name, score):
    client = MongoClient("127.0.0.1", 27017)
    Practice = client.Practice
    P_ranking = Practice.P_ranking

    ranking = {"name": name,
               "score": score}
    P_ranking.insert_one(ranking)


def R_reg():
    client = MongoClient("127.0.0.1", 27017)
    Random = client.Random
    R_ranking = Random.R_ranking

    ranking = {"name": "test",
               "score": "211"}
    R_ranking.insert_one(ranking)


def P_ranking(score):
    client = MongoClient("127.0.0.1", 27017)

    Practice = client.Practice
    P_ranking = Practice.P_ranking
    count = 0
    mydoc = P_ranking.find().sort("score", -1)
    for x in mydoc:
        count += 1
        if x["score"] == score:
            return count
