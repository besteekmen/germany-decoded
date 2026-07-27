from germany_decoded.ingestion import load_law_index


def main():
    print("Downloading official German law index...")

    root = load_law_index()

    print("Success!")
    print(root.tag)


if __name__ == "__main__":
    main()