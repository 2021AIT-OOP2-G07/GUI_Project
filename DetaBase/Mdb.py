
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


def P_result(score):
    client = MongoClient("127.0.0.1", 27017)

    ResultData = client.Practice.P_ranking
    # count = 0
    ret = ResultData.count_documents(filter={"score": {"$gt": score}})
    return ret+1


def R_result(score):
    client = MongoClient("127.0.0.1", 27017)

    ResultData = client.Random.R_ranking
    ret = ResultData.count_documents(filter={"score": {"$gt": score}})
    return ret+1


def P_ranking():
    client = MongoClient("127.0.0.1", 27017)
    RankingData = client.Practice.P_ranking
    ranking = []
    mydoc = RankingData.find().sort("score", -1)
    for x in mydoc:
        ranking.append({"name": x['name'], "score": x['score']})
    return ranking


def R_ranking():
    client = MongoClient("127.0.0.1", 27017)
    RankingData = client.Random.R_ranking
    ranking = []
    mydoc = RankingData.find().sort("score", -1)
    for x in mydoc:
        ranking.append({"name": x['name'], "score": x['score']})
    return ranking


a = R_ranking()
print(a)
