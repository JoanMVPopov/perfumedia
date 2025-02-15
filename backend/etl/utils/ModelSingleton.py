import gc
import os
import sys
from html import unescape

import numpy as np
import psutil
import torch
import unicodedata
from sentence_transformers import CrossEncoder
from pathlib import Path
from torch.quantization import quantize_dynamic

BASE_DIR = Path(__file__).resolve().parent  # Get the script's directory
MODEL_PATH = os.path.join(BASE_DIR, "cross-miniLM-perfumedia-finetuned")

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Model(metaclass=Singleton):
    def __init__(self):
        self._model = CrossEncoder(MODEL_PATH, device='cpu')
        torch.set_num_threads(2)

        quantized_model = quantize_dynamic(
            self._model.model,
            {torch.nn.Linear},
            dtype=torch.qint8
        )
        self._model.model = quantized_model
        torch.inference_mode(True)

    def get_size(self, obj):
        """Returns size of object in bytes"""
        return sys.getsizeof(obj)

    def log_memory(self, label=""):
        """Log current memory usage"""
        process = psutil.Process()
        print(f"{label} Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")

    def sanitize_query(self, query):
        # Convert to string if not already
        query = str(query)
        # Remove HTML entities
        query = unescape(query)
        # Normalize unicode characters
        query = unicodedata.normalize('NFKD', query)
        # Remove extra spaces and trim
        query = ' '.join(query.split())
        # Convert to lowercase
        query = query.lower()

        return query

    def calculate_similarity(self, query, data):
        try:
            self.log_memory("Before similarity calculation")

            sanitized_query = self.sanitize_query(query)
            with torch.inference_mode():
                ranks = self._model.rank(sanitized_query, data)

                # Force garbage collection
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()

                # Clear any cached tensors
                #if hasattr(self._model, 'clear_cache'):
                # self._model.

                self.log_memory("After similarity calculation")

                # Get size of ranks
                ranks_size = self.get_size(ranks)
                print(f"Ranks object size: {ranks_size / 1024:.2f} KB")

                model_size = self.get_size(self._model)
                print(f"Model object size: {model_size / 1024:.2f} KB")

                return ranks
        except Exception as e:
            print(e)