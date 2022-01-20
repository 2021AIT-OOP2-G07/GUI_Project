
from pymongo import MongoClient


def P_reg(name, score):
    client = MongoClient("127.0.0.1", 27017)
    Practice = client.Practice
    P_ranking = Practice.P_ranking

    ranking = {"name": name,
               "score": score}
    P_ranking.insert_one(ranking)


def R_reg(name, score):
    client = MongoClient("127.0.0.1", 27017)
    Random = client.Random
    R_ranking = Random.R_ranking

    ranking = {"name": name,
               "score": score}
    R_ranking.insert_one(ranking)


def P_ranking(score):
    client = MongoClient("127.0.0.1", 27017)

    Practice = client.Practice
    P_ranking = Practice.P_ranking
    # count = 0
    ret = P_ranking.count_documents(filter={"score": {"$gt": score}})
    return ret+1
