from langchain import OpenAI, LLMChain

from biogen.chain import ModelChain
from biogen.templates import READ_JSON_TEMPLATE, READ_CURRICULUM_TEMPLATE, \
    GENERATE_BIO_TEMPLATE


class APIModel:
    def __init__(
            self,
            model_name: str = "text-davinci-003",
            temperature: float = 0.7,
            max_tokens: int = 2048,
    ):
        llm = OpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
        website_chain = LLMChain(llm=llm, prompt=READ_JSON_TEMPLATE)
        curriculum_chain = LLMChain(llm=llm, prompt=READ_CURRICULUM_TEMPLATE)
        generation_bio_chain = LLMChain(llm=llm, prompt=GENERATE_BIO_TEMPLATE)
        self._chain = ModelChain(
            json_reader=website_chain,
            curriculum_reader=curriculum_chain,
            llm_core=generation_bio_chain,
        )

    def __call__(self, website_json: str, curriculum: str) -> str:
        return self._chain.run(
            webpage=website_json,
            curriculum=curriculum
        )


if __name__ == "__main__":
    model = APIModel()
    print(model("website_json", "curriculum"))