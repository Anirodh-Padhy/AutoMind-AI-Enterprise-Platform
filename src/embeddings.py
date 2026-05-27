from sentence_transformers import SentenceTransformer

import faiss
import numpy as np

# ===================================================
# LOAD EMBEDDING MODEL
# ===================================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ===================================================
# CREATE CHUNKS
# ===================================================

def create_chunks(

    text,

    chunk_size=500
):

    chunks = []

    for i in range(

        0,

        len(text),

        chunk_size
    ):

        chunk = text[
            i:i + chunk_size
        ]

        chunks.append(chunk)

    return chunks

# ===================================================
# CREATE VECTOR STORE
# ===================================================

def create_vector_store(text):

    chunks = create_chunks(text)

    embeddings = embedding_model.encode(
        chunks
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        np.array(embeddings)
    )

    return index, chunks

# ===================================================
# SEARCH DOCUMENTS
# ===================================================

def search_documents(

    query,

    index,

    chunks,

    top_k=3
):

    query_embedding = embedding_model.encode(
        [query]
    )

    distances, indices = index.search(

        np.array(query_embedding),

        top_k
    )

    retrieved_chunks = []

    for idx in indices[0]:

        retrieved_chunks.append(
            chunks[idx]
        )

    return retrieved_chunks