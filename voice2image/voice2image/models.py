import re
from abc import abstractmethod, ABC

import openai


class BaseOpenAIModel(ABC):
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError


class WhisperModel(BaseOpenAIModel):
    def __init__(self, model_name: str, verbose: bool = False):
        super().__init__(verbose=verbose)
        self.model = model_name

    def run(self, file_path: str):
        if self.verbose:
            print(f"Transcribing audio file: {file_path}")
        audio_file = open(file_path, "rb")
        transcript = openai.Audio.transcribe(self.model, audio_file)
        if self.verbose:
            print(f"Transcript output: {transcript}")
        return transcript["text"]


class PromptGenerationModel(BaseOpenAIModel):
    SYSTEM_TEMPLATE = {
        "role": "system",
        "content": (
            "You are an AI assistant whose main goal is to help people in "
            "creating amazing prompts to be used for generating images. In "
            "order to generate images the user will use DALLE2 model, "
            "developed by OpenAI. The user will provide you with an "
            "initial prompt and you will have to help him/her to create "
            "a better one. Generate the prompt with the following "
            "format: <begin> <prompt> <end>. The <begin> and <end> "
            "tokens are used to mark the beginning and the end of the "
            "prompt. The <prompt> token is used to mark the part of the "
            "prompt that will be used to generate the image. You must write "
            "the prompt in english even if the user provides you with a "
            "prompt in another language."
        )
    }

    def run(self, user_input):
        if self.verbose:
            print(f"User input: {user_input}")
        user_message = {
            "role": "user",
            "content": user_input,
        }
        messages = [self.SYSTEM_TEMPLATE, user_message]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        if self.verbose:
            print(f"OpenAI response: {response}")
        model_response = response["choices"][0]["message"]["content"]
        # write a regex to extract the prompt
        regex = r"<begin> (.*) <end>"
        prompt = re.search(regex, model_response).group(0)
        if self.verbose:
            print(f"Prompt: {prompt}")
        return prompt


class ImageGenerationModel(BaseOpenAIModel):
    def __init__(self, n_images: int = 1, verbose: bool = False):
        super().__init__(verbose=verbose)
        self.n_images = n_images

    def run(self, prompt: str):
        if self.verbose:
            print(f"Prompt: {prompt}")
        response = openai.Image.create(
            prompt=prompt,
            n=self.n_images,
            # size="1024x1024"
            size="512x512"
        )
        if self.verbose:
            print(f"OpenAI response: {response}")
        image_urls = response['data']
        return [x['url'] for x in image_urls]
