import faiss
import numpy as np
import ollama
import pickle
import os

# Function to load the HPO embedding database
def load_hpo_embedding_db(pkl_file_path): 
    # Load the HPO embedding database from the file
    with open(pkl_file_path, 'rb') as f:
        hpo_embed_db = pickle.load(f)
    
    # Assign global variables for later use
    global terms, hpo_index, hpo_embeddings
    terms = hpo_embed_db["hpo_terms"]
    hpo_embeddings = hpo_embed_db["hpo_embeddings"]
    hpo_index = faiss.IndexFlatL2(hpo_embeddings.shape[1])
    hpo_index.add(hpo_embeddings)
    return hpo_embed_db

   
def retrieve_similar_terms(query, k=3):
#    similar_terms = [('HP:0000737', 'Irritability', 0.0),
# ('HP:0033628', 'Bowel irritability', 125.82888),
# ('HP:0031588', 'Unhappy demeanor', 130.33144)]
    query_vec = np.array(list(ollama.embeddings(model='mxbai-embed-large', prompt=query).values())[0], dtype=np.float32)
    query_vec = query_vec.reshape(1, -1)
    distances, indices = hpo_index.search(query_vec, k)
    similar_terms = [(list(terms.keys())[i], list(terms.values())[i], distances[0][j]) for j, i in enumerate(indices[0])]
    return similar_terms


