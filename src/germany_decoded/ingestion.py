from germany_decoded.loaders.bgb import load_bgb

def load_documents():
    """
    Load all resources.
    """
    documents = []
    documents.extend(load_bgb())
    # documents.extend(load_beratungshilfe())
    # documents.extend(load_aufenthaltsgesetz())

    return documents