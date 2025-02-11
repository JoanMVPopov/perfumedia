import os
from sentence_transformers import CrossEncoder

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Model(metaclass=Singleton):
    def __init__(self):
        path = os.path.join(os.getcwd(), "cross-miniLM-perfumedia-finetuned")
        self._model = CrossEncoder(path)

    def calculate_similarity(self, query, data):
        ranks = self._model.rank(query, data)

        rank_score_first = ranks[0]['score']

        # invert results for negation
        if rank_score_first <= 0:
            ranks = ranks[::-1]

        indices_to_return = []

        # return top 20
        for rank in ranks[:20]:
            score = rank['score']
            index = rank['corpus_id']
            indices_to_return.append(index)
            #print(f"{score:.2f}\n{data.iloc[index]['name']}\n---------\n")

        return indices_to_return