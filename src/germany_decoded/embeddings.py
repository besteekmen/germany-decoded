from sentence_transformers import SentenceTransformer

# load a pretrained sentence transformer model
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
_model = None


def get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)

    return _model

def create_embeddings(documents):
    model = get_model()

    texts = [
        doc["content"]
        for doc in documents
    ]

    return model.encode(
        texts,
        normalize_embeddings=True
    )

def embed_query(query):
    model = get_model()
    
    return model.encode(
        query,
        normalize_embeddings=True
    )