import sys

import json
from pathlib import Path

import conllu


def get_output_path(input_path):
    parts = input_path.stem.split(".")
    base_dir = Path(f"data/syntax-trees/{parts[0]}/{parts[1]}/processed")
    base_dir.mkdir(parents=True, exist_ok=True)
    return Path(base_dir, f"{input_path.stem}.json")


def main():
    input_path = Path(sys.argv[1])
    version = sys.argv[2]

    data = conllu.parse(input_path.read_text())
    meta = {}
    to_create = []
    counter = 0
    for sentence in data:
        counter += 1
        meta.update(sentence.metadata)
        new_obj = {}
        new_obj.update(meta)

        seen_urns = set()
        # FIXME: `sent_id` may not be required
        # sentence_id = int(new_obj["sent_id"].split("@")[1])
        sentence_id = counter

        sentence_obj = {
            "urn": f"urn:cite2:scaife-viewer:syntaxTree.v1:syntaxTree{sentence_id}",
            "treebank_id": sentence_id,
            "words": [],
        }
        for token in sentence:
            word_obj = {
                "id": token["id"],
                "value": token["form"],
                "head_id": token["head"],
                "relation": token["deprel"],
            }
            sentence_obj["words"].append(word_obj)

        # TODO: can't do cite or refs just yet, which will be required
        # This is likely something we could do from that sent_id as another
        # kind of lookup
        sentence_obj.update(
            {
                "references": [],
                "citation": str(sentence_id),
            }
        )
        to_create.append(sentence_obj)

    output_path = get_output_path(input_path)

    json.dump(
        to_create,
        open(output_path, "w"),
        ensure_ascii=False,
        indent=2,
    )


if __name__ == "__main__":
    main()
