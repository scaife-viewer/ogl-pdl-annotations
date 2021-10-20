import sys

from pathlib import Path

import spacy

from spacy_conll import init_parser


def extract_content(path):
    # https://github.com/BramVanroy/spacy_conll/issues/9
    txt = []
    if path.suffix == ".txt":
        for l in path.read_text().splitlines():
            ref, content = l.split(" ", maxsplit=1)

            txt.append(content.strip())
    elif path.suffix == ".cex":
        for l in path.read_text().splitlines():
            ref, content = l.split("#", maxsplit=1)

            txt.append(content.strip())

    return " ".join(txt)


def get_output_path(input_path):
    parts = input_path.stem.split(".")
    base_dir = Path(f"data/syntax-trees/{parts[0]}/{parts[1]}/raw")
    base_dir.mkdir(parents=True, exist_ok=True)
    return Path(base_dir, f"{input_path.stem}.conllu")


def main():
    """
    TODO: Ensure we're programatically picking up any of the
    required Spacy or Stanza data models when we're packaging or
    deploying this project
    """
    # TODO: revisit these parsers

    # Stanza
    nlp = init_parser(
        "en",
        "stanza",
    )
    # Spacy parser
    # nlp = init_parser(
    #     "en_core_web_sm",
    #     "spacy",
    # )

    # UD-Pipe
    # nlp = init_parser(
    #     "en",
    #     "udpipe",
    # )

    # TODO: document path; files aren't in this local
    # repo yet
    input_path = Path(sys.argv[1])
    content = extract_content(input_path)
    doc = nlp(content)

    output_path = get_output_path(input_path)
    output_path.write_text(doc._.conll_str)


if __name__ == "__main__":
    main()
