from pathlib import Path

import spacy

from spacy_conll import init_parser


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

    # TODO: This file does not exist in VCS
    input_path = Path("data/tlg0012.tlg001.parrish-eng1.txt")
    # https://github.com/BramVanroy/spacy_conll/issues/9
    txt = " ".join([l.strip() for l in input_path.read_text().splitlines()])
    doc = nlp(txt)
    output_path = Path("data/syntax-trees/tlg0012/tlg001/raw/tlg0012.tlg001.parrish-eng1.conllu")
    output_path.write_text(doc._.conll_str)


if __name__ == "__main__":
    main()
