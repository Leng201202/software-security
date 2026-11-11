"""Emit a CycloneDX 1.5 SBOM of the declared pinned requirements.
Offline direct-component inventory only: not an installed-image or full resolved
transitive inventory, and not a vulnerability/provenance assessment.
python3 sbom_core.py > sbom-core.cdx.json  # use an output path outside tracked source
"""
from pathlib import Path
import json
import re
import sys

def inventory(requirements):
    components = []
    for raw in requirements.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        match = re.fullmatch(r"([A-Za-z0-9_.-]+)==([A-Za-z0-9_.+!-]+)", line)
        if match is None:
            raise ValueError("This bounded inventory accepts pinned name==version lines only")
        name, version = match.groups()
        canonical = re.sub(r"[-_.]+", "-", name).lower()
        purl = "pkg:pypi/" + canonical + "@" + version
        components.append({"type": "library", "bom-ref": purl, "name": name,
                           "version": version, "purl": purl})
    return {"bomFormat": "CycloneDX", "specVersion": "1.5", "version": 1,
            "metadata": {"properties": [{"name": "course:inventory-scope",
                "value": "declared pinned direct components; not an installed/transitive inventory"}]},
            "components": components}

if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("requirements.txt")
    print(json.dumps(inventory(path.read_text()), indent=2))
