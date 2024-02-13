from pymongo import MongoClient
from pprint import pprint


client = MongoClient('localhost', 27017)
db = client['mirClima']

mircli = db.mircli


def searcj_all():
    list_search = []
    for i in mircli.find({}, {'_id': False}):
        list_search.append(i)
    return list_search


ls = [i for i in range(12, 22)]

def en_ls(ls):
    for i, x in enumerate(ls):
        print(i, x)

if __name__ == '__main__':
    pprint(searcj_all())
    # en_ls(ls)