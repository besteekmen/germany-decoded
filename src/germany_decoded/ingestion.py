import requests
from lxml import etree

from gesetze_im_internet import toc


def load_documents():
    """
    Load selected German law sections.

    Source:
    https://www.gesetze-im-internet.de/
    """

    bgb = toc("Bürgerliches Gesetzbuch")

    sections = [
        535,  # Mietvertrag
        536,  # Mietminderung
        537,  # Entrichtung der Miete
    ]

    documents = []

    for number in sections:
        section = bgb(number)

        documents.append(
            {
                "title": f"BGB § {number}",
                "content": str(section),
                "source": section.href,
                "law": "Bürgerliches Gesetzbuch",
                "language": "de",
            }
        )

    return documents