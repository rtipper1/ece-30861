"""
license.py

Class for storage and calculation of license metric. 

Inherits from metric.py

Scoring:
- 0 = no license listed
- 1 = fully open (Apache-2.0, MIT, BSD)
- 0.8 = open but with some restrictions (e.g., LGPL, CC-BY)
- 0.6 = research/evaluation-only or non-commercial
- 0.4 = fallback when license string exists but is unknown
- 0.2 = proprietary/closed
"""

level_5_licenses = ["apache-2.0", "mit", "bsd", "bsd-2-clause", "bsd-3-clause",
    "bsd-3-clause-clear", "isc", "zlib", "unlicense", "cc0-1.0",
    "wtfpl", "postgresql", "ncsa", "afl-3.0", "artistic-2.0",
    "ecl-2.0", "mpl-2.0", "ms-pl", "etalab-2.0", "odc-by",
    "odbl", "eupl-1.1", "eupl-1.2", "epl-1.0", "epl-2.0",
    "lppl-1.3c", "ofl-1.1", "pddl", "cdla-permissive-1.0",
    "cdla-permissive-2.0", "cdla-sharing-1.0"]

level_4_licenses = ["lgpl", "lgpl-2.1", "lgpl-3.0", "cc-by-4.0", "cc-by-3.0",
    "cc-by-2.0", "cc-by-2.5", "cc-by-sa-4.0", "cc-by-sa-3.0",
    "cc", "osl-3.0", "bsl-1.0", "gpl", "gpl-2.0", "gpl-3.0",
    "agpl-3.0", "gfdl"]

level_3_licenses = ["cc-by-nc-4.0", "cc-by-nc-3.0", "cc-by-nc-2.0", "cc-by-nc-sa-4.0",
    "cc-by-nc-sa-3.0", "cc-by-nc-sa-2.0", "cc-by-nc-nd-4.0",
    "cc-by-nc-nd-3.0", "fair-noncommercial-research-license",
    "intel-research", "h-research"]

level_2_licenses = ["openrail", "openrail++", "creativeml-openrail-m", "bigscience-bloom-rail-1.0",
    "bigscience-openrail-m", "bigcode-openrail-m", "deepfloyd-if-license",
    "apple-amlr", "apple-ascl", "lgpl-lr", "open-mdw", "c-uda"]

level_1_licenses = ["llama2", "llama3", "llama3.1", "llama3.2", "llama3.3",
    "llama4", "gemma"]

from metrics.metric import Metric

class LicenseMetric(Metric):
    def __init__(self):
        super().__init__("license")

    def calcualte_score(self) -> float:
        license = self.data["license"]

        match license.lower() if license else "":
            case l if l in level_5_licenses:
                return 1.0
            case l if l in level_4_licenses:
                return 0.8
            case l if l in level_3_licenses:
                return 0.6
            case l if l in level_2_licenses:
                return 0.4
            case l if l in level_1_licenses:
                return 0.2
            case _:
                return 0.0