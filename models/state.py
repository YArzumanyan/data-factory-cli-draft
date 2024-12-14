from typing import Dict


class PipelineState:
    def __init__(self, latest_version: int, versions: Dict[int, str]):
        self.latest_version = latest_version
        self.versions = versions

    def to_dict(self):
        return {
            "latest_version": self.latest_version,
            "versions": self.versions
        }

    @staticmethod
    def from_dict(data: Dict):
        return PipelineState(data["latest_version"], data["versions"])