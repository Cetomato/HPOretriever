import faiss
import numpy as np
import ollama
import pickle
import os
import requests

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

# Function for retrieve_similar_terms
def retrieve_similar_terms(query, k=3):
#    similar_terms = [('HP:0000737', 'Irritability', 0.0),
# ('HP:0033628', 'Bowel irritability', 125.82888),
# ('HP:0031588', 'Unhappy demeanor', 130.33144)]
    query_vec = np.array(list(ollama.embeddings(model='mxbai-embed-large', prompt=query).values())[0], dtype=np.float32)
    query_vec = query_vec.reshape(1, -1)
    distances, indices = hpo_index.search(query_vec, k)
    similar_terms = [(list(terms.keys())[i], list(terms.values())[i], distances[0][j]) for j, i in enumerate(indices[0])]
    return similar_terms

# Extract words related to AE
def get_ae_words(ae_text):
    ollama_url = "http://localhost:11434/api/generate"
#   ae_text = "• The most commonly reported solicited local and systemic adverse reactions in pregnant individuals (≥10%) were pain at the injection site (40.6%), headache (31.0%), muscle pain (26.5%), and nausea (20.0%). (6.1) • The most commonly reported solicited local and systemic adverse reactions in individuals 60 years of age and older (≥10%) were fatigue (15.5%), headache (12.8%), pain at the injection site (10.5%), and muscle pain (10.1%). (6.1)"
    get_ae_words_prompt = (
    f"In the text: '{ae_text}', extract all unique Adverse Reaction terms directly, in lowercase, and return them in a single line separated by commas. "
    f"Do not add any extra words, phrases, or explanations; only return the terms themselves. Do not include any introductory pharases like 'Here are the unique Adverse Reaction terms directly extracted from the input text:'"
    f"\n\nExample:\n"
    f"Input text: '• Most common local adverse reactions in ≥20% of subjects were pain, redness, and swelling at the injection site. (6.1) • Most common general adverse events in ≥20% of subjects were fatigue, headache, myalgia, gastrointestinal symptoms, and arthralgia. (6.1)'"
    f"\nOutput text: 'pain, redness, swelling at the injection site, fatigue, headache, myalgia, gastrointestinal symptoms, arthralgia'"
)

    payload = {
        "model": "llama3.1",
        "prompt": get_ae_words_prompt,
        "stream": False
    }

    response = requests.post(ollama_url, json=payload)

    if response.status_code == 200:
        ae_words = response.json().get('response', '')
        ae_words_list = [word.strip() for word in ae_words.split(',')]
        return ae_words_list
    else:
        print("Failed to retrieve AE words. Status code:", response.status_code)
        return []

# ae_text = "• The most commonly reported solicited local and systemic adverse reactions in pregnant individuals (≥10%) were pain at the injection site (40.6%), headache (31.0%), muscle pain (26.5%), and nausea (20.0%). (6.1) • The most commonly reported solicited local and systemic adverse reactions in individuals 60 years of age and older (≥10%) were fatigue (15.5%), headache (12.8%), pain at the injection site (10.5%), and muscle pain (10.1%). (6.1)"
# get_ae_words(ae_text)





