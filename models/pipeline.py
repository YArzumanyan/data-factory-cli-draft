from typing import List, Dict, Union, Optional

class PipelineNode:
    def __init__(
        self, 
        node_id: str, 
        node_type: str, 
        script_id: Optional[str] = None, 
        dataset_id: Optional[str] = None, 
        path: Optional[str] = None
    ):
        self.id = node_id
        self.type = node_type  # "script" or "dataset"
        self.script_id = script_id
        self.dataset_id = dataset_id
        self.path = path

class PipelineEdge:
    def __init__(self, from_node: str, to_node: str, arguments: List[Union[str, Dict[str, str]]] = []):
        self.from_node = from_node
        self.to_node = to_node
        self.arguments = arguments

class Pipeline:
    def __init__(self, pipeline_id: str, nodes: List[PipelineNode], edges: List[PipelineEdge]):
        self.id = pipeline_id
        self.nodes = nodes
        self.edges = edges

    def to_dict(self):
        return {
            "id": self.id,
            "nodes": [
                {
                    "id": node.id,
                    "type": node.type,
                    **({"script_id": node.script_id} if node.script_id else {}),
                    **({"dataset_id": node.dataset_id} if node.dataset_id else {}),
                    **({"path": node.path} if node.path else {})
                }
                for node in self.nodes
            ],
            "edges": [
                {
                    "from": edge.from_node,
                    "to": edge.to_node,
                    "arguments": edge.arguments
                }
                for edge in self.edges
            ]
        }

    @staticmethod
    def from_dict(data: Dict):
        nodes = [
            PipelineNode(
                node_id=node["id"],
                node_type=node["type"],
                script_id=node.get("script_id"),
                dataset_id=node.get("dataset_id"),
                path=node.get("path")
            )
            for node in data["nodes"]
        ]
        edges = [
            PipelineEdge(
                from_node=edge["from"],
                to_node=edge["to"],
                arguments=edge.get("arguments", [])
            )
            for edge in data["edges"]
        ]
        return Pipeline(data["id"], nodes, edges)
