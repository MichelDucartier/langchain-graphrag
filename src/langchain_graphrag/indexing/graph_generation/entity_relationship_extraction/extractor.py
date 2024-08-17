"""Entity Relationship Extractor module."""

from __future__ import annotations

import logging

import networkx as nx
import pandas as pd
from langchain_core.language_models import BaseLLM
from tqdm import tqdm

from langchain_graphrag.types.prompts import PromptBuilder

from .prompt_builder import EntityExtractionPromptBuilder

_LOGGER = logging.getLogger(__name__)


class EntityRelationshipExtractor:
    def __init__(self, prompt_builder: PromptBuilder, llm: BaseLLM):
        """Extracts entities and relationships from text units using a language model.

        Args:
            prompt_builder (PromptBuilder): The prompt builder object used to construct the prompt for the language model.
            llm (BaseLLM): The language model used for entity and relationship extraction.

        """
        prompt, output_parser = prompt_builder.build()
        self._extraction_chain = prompt | llm | output_parser
        self._prompt_builder = prompt_builder

    @staticmethod
    def build_default(llm: BaseLLM) -> EntityRelationshipExtractor:
        """Builds and returns an instance of EntityRelationshipExtractor with default parameters.

        Parameters:
            llm (BaseLLM): The BaseLLM object used for entity relationship extraction.

        Returns:
            EntityRelationshipExtractor: An instance of EntityRelationshipExtractor with default parameters.
        """
        return EntityRelationshipExtractor(
            prompt_builder=EntityExtractionPromptBuilder(),
            llm=llm,
        )

    def invoke(self, text_units: pd.DataFrame) -> list[nx.Graph]:
        """Invoke the entity relationship extraction process on the text units.

        Parameters:
            text_units (pd.DataFrame): A pandas dataframe containing the text units.

        Returns:
            A list of networkx Graph objects representing the extracted entities and relationships.
        """

        def _run_chain(series: pd.Series) -> nx.Graph:
            _, text_id, text_unit = (
                series["document_id"],
                series["id"],
                series["text"],
            )

            chain_input = self._prompt_builder.prepare_chain_input(text_unit=text_unit)

            chunk_graph = self._extraction_chain.invoke(input=chain_input)

            # add the chunk_id to the nodes
            for node_names in chunk_graph.nodes():
                chunk_graph.nodes[node_names]["text_unit_ids"] = [text_id]

            # add the chunk_id to the edges as well
            for edge_names in chunk_graph.edges():
                chunk_graph.edges[edge_names]["text_unit_ids"] = [text_id]

            if logging.getLevelName(_LOGGER.getEffectiveLevel()) == "DEBUG":
                _LOGGER.debug(f"Graph for: {text_id}")
                _LOGGER.debug(chunk_graph)

            return chunk_graph

        tqdm.pandas(desc="Extracting entities and relationships ...")
        chunk_graphs: list[nx.Graph] = text_units.progress_apply(_run_chain, axis=1)

        return chunk_graphs
