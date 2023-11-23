import pandas as pd
import numpy as np
import torch
from transformers import BertTokenizer, BertModel
import spacy
import inflect
import re 
from scipy.sparse import save_npz, load_npz
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import streamlit as st
import pandas as pd


merged_anime= pd.read_csv('merged_anime.csv')

anime_pivot = pd.read_csv('anime_pivot.csv')

anime_pivot_reversed = pd.read_csv('anime_pivot_reversed.csv') 

anime_pivot_reversed_sparse = load_npz('anime_pivot_reversed_sparse.npz')

knn = NearestNeighbors(n_neighbors=9,algorithm= 'brute', metric= 'cosine')

model_knn = knn.fit(anime_pivot_reversed_sparse)

