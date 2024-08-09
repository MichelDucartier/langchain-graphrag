from typing import NamedTuple

import pandas as pd

from langchain_graphrag.indexing.artifacts import IndexerArtifacts

from .entities import EntitiesSelector
from .relationships import RelationshipsSelectionResult, RelationshipsSelector
from .text_units import TextUnitsSelector


class ContextSelectionResult(NamedTuple):
    entities: pd.DataFrame
    text_units: pd.DataFrame
    relationships: RelationshipsSelectionResult


class ContextSelector:
    def __init__(
        self,
        entities_selector: EntitiesSelector,
        text_units_selector: TextUnitsSelector,
        relationships_selector: RelationshipsSelector,
    ):
        self._entities_selector = entities_selector
        self._text_units_selector = text_units_selector
        self._relationships_selector = relationships_selector

    def run(
        self,
        query: str,
        artifacts: IndexerArtifacts,
    ):
        # Step 1
        # Select the entities to be used in the local search
        selected_entities = self._entities_selector.run(query, artifacts.entities)

        # Step 2
        # Select the text units to be used in the local search
        selected_text_units = self._text_units_selector.run(
            df_entities=selected_entities,
            df_relationships=artifacts.relationships,
            df_text_units=artifacts.text_units,
        )

        # Step 3
        # Select the relationships to be used in the local search
        selected_relationships = self._relationships_selector.run(
            df_entities=selected_entities,
            df_relationships=artifacts.relationships,
        )

        return ContextSelectionResult(
            entities=selected_entities,
            text_units=selected_text_units,
            relationships=selected_relationships,
        )