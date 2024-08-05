import networkx as nx
from langchain_core.language_models import BaseLLM
from langchain_core.output_parsers.base import BaseOutputParser
from tqdm import tqdm

from langchain_graphrag.types.prompts import PromptBuilder


class EntityRelationshipDescriptionSummarizer:
    def __init__(
        self,
        prompt_builder: PromptBuilder,
        llm: BaseLLM,
        output_parser: BaseOutputParser,
    ):
        prompt = prompt_builder.build()
        self._summarize_chain = prompt | llm | output_parser
        self._prompt_builder = prompt_builder

    def invoke(self, graph: nx.Graph) -> nx.Graph:
        for node_name, node in tqdm(
            graph.nodes(data=True), desc="Summarizing entities descriptions"
        ):
            if len(node["description"]) == 1:
                node["description"] = node["description"][0]
                continue

            chain_input = self._prompt_builder.prepare_chain_input(
                entity_name=node_name, description_list=node["description"]
            )

            node["description"] = self._summarize_chain.invoke(input=chain_input)

        for from_node, to_node, edge in tqdm(
            graph.edges(data=True), desc="Summarizing relationship descriptions"
        ):
            if len(edge["description"]) == 1:
                edge["description"] = edge["description"][0]
                continue

            chain_input = self._prompt_builder.prepare_chain_input(
                entity_name=f"{from_node} -> {to_node}",
                description_list=edge["description"],
            )

            edge["description"] = self._summarize_chain.invoke(input=chain_input)

        return graph
