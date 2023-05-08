from typing import Dict, List

from langchain import LLMChain
from langchain.chains.base import Chain
from pydantic import BaseModel


class ModelChain(Chain, BaseModel):
    json_reader: LLMChain
    curriculum_reader: LLMChain
    llm_core: LLMChain
    output_key: str = "text"
    curriculum_key: str = "curriculum"
    json_key: str = "webpage"

    @property
    def _chain_type(self) -> str:
        pass

    @property
    def input_keys(self) -> List[str]:
        keys = (
            self.json_reader.input_keys +
            self.curriculum_reader.input_keys +
            self.llm_core.input_keys
        )
        return list(set(keys))

    @property
    def output_keys(self) -> List[str]:
        return [self.output_key]

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        json_inputs = {
            key: value for key, value in inputs.items()
            if key in self.json_reader.input_keys
        }
        json_output = self.json_reader.run(**json_inputs)
        curriculum_inputs = {
            key: value for key, value in inputs.items()
            if key in self.curriculum_reader.input_keys
        }
        curriculum_output = self.curriculum_reader.run(**curriculum_inputs)
        inputs.update({
            self.json_key: json_output,
            self.curriculum_key: curriculum_output
        })
        llm_core_output = self.llm_core.run(**inputs)
        return {self.output_key: llm_core_output}

