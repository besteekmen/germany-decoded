from gesetze_im_internet import toc

TENANCY_START = 535.0
TENANCY_END = 580.99

def load_bgb():
    """
    Load tenancy-related sections from the German Civil Code (BGB).

    Source:
    https://www.gesetze-im-internet.de/
    """

    bgb = toc("Bürgerliches Gesetzbuch")
    documents = []

    for norm in bgb:
        # skip table of contents
        if not norm.enbez:
            continue
        
        # skip removed sections
        if "weggefallen" in norm.enbez.lower():
            continue
        if norm.nr is None:
            continue

        # keep only tenancy law (§§ 535–580a)
        section = float(norm.nr)
        if not (TENANCY_START <= section <= TENANCY_END):
            continue

        documents.append(
            {
                "law": "BGB",
                "section": norm.enbez,
                "title": norm.titel,
                "content": str(norm),
                "source": norm.href,
                "language": "de",
            }
        )

    return documents