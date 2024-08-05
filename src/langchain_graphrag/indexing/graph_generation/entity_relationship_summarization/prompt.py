from pathlib import Path
from typing import Any

from langchain_core.prompts import PromptTemplate

from langchain_graphrag.types.prompts import PromptBuilder


class DefaultSummarizeDescriptionPromptBuilder(PromptBuilder):
    def __init__(self, prompt_path: Path):
        self._prompt_path = prompt_path

    def build(self) -> PromptTemplate:
        return PromptTemplate.from_file(self._prompt_path)

    def prepare_chain_input(self, **kwargs: dict[str, Any]) -> dict[str, str]:
        entity_name = kwargs.get("entity_name", None)
        description_list = kwargs.get("description_list", None)
        if entity_name is None:
            raise ValueError("entity_name is required")
        if description_list is None:
            raise ValueError("description_list is required")

        return dict(description_list=description_list, entity_name=entity_name)
