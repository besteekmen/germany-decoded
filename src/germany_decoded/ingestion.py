import requests
from lxml import etree

LAW_INDEX_URL = "https://www.gesetze-im-internet.de/gii-toc.xml"

def load_law_index():
    """Download and parse the official German law index."""
    response = requests.get(LAW_INDEX_URL, timeout=30)
    response.raise_for_status()

    root = etree.fromstring(response.content)
    return root

def load_documents():
    """Load all knowledge base documents."""

    documents = []

    # TODO: #1 Add sources here one by one
    
    return documents

def build_index(documents):
    index = Index(
        text_fields=["question", "section", "answer"],
        keyword_fields=["course"]
    )
    index.fit(documents)
    return index