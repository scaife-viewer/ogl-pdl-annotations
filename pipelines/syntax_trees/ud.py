import json
from pathlib import Path

import conllu


def main():
    path = Path("data/syntax-trees/tlg0012/tlg001/raw/tlg0012.tlg001.parrish-eng1.conllu")
    data = conllu.parse(open(path).read())

    version = "urn:cts:greekLit:tlg0012.tlg001.parrish-eng1:"
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
            {"references": [], "citation": str(sentence_id),}
        )
        to_create.append(sentence_obj)

    output_path = Path("data/syntax-trees/tlg0012/tlg001/processed/tlg0012.tlg001.parrish-eng1.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    json.dump(
        to_create,
        open(output_path, "w"),
        ensure_ascii=False,
        indent=2,
    )


if __name__ == "__main__":
    main()
