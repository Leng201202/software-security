"""Offline bounded resolver teaching model, NOT pip's complete resolver.
Only three-part numeric versions and one package are modelled. No package is
installed; real resolution additionally considers constraints, compatibility,
pre-releases and dependency graphs. Index trust is separate from version size.
"""
import argparse
import json
import re

def choose(mode, private, public):
    def version(text):
        if not re.fullmatch(r"[0-9]+[.][0-9]+[.][0-9]+", text):
            raise ValueError("Use numeric major.minor.patch in this bounded case")
        return tuple(map(int, text.split(".")))
    candidates = [("private", private)] if mode == "single" else [("private", private), ("public", public)]
    index, selected = max(candidates, key=lambda pair: version(pair[1]))
    return {"model": "bounded single-package numeric-version comparison", "mode": mode,
            "selected_index": index, "selected_version": selected,
            "trust_note": "higher version alone does not establish publisher trust"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["merged", "single"], required=True)
    parser.add_argument("--private", default="1.4.0")
    parser.add_argument("--public", default="99.0.0")
    args = parser.parse_args()
    print(json.dumps(choose(args.mode, args.private, args.public), indent=2))
