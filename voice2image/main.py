import os
import gradio as gr

from voice2image.models import (
    WhisperModel, PromptGenerationModel, ImageGenerationModel
)

debug = True
whisper_model = WhisperModel("whisper-1", verbose=debug)
prompt_generation_model = PromptGenerationModel(verbose=debug)
image_generation_model = ImageGenerationModel(n_images=4, verbose=debug)


def convert_audio(audio_file):
    os.rename(audio_file, audio_file + '.wav')
    transcript = whisper_model(audio_file + '.wav')
    prompt = prompt_generation_model(transcript)
    images = image_generation_model(prompt)
    return images


with gr.Blocks() as demo:
    # Add a title
    gr.Markdown(
        "# 🚀Voice2Image🚀\n\nThe Voice2Image app allows you to convert audio "
        "to images. You can use the microphone to record your voice and then "
        "generate images based on the audio you recorded.\n\nEnjoy!🔥"
    )
    audio_window = gr.Audio(
        source="microphone", type="filepath", label="Input Audio"
    )
    convert_button = gr.Button("Generate Images")
    with gr.Row():
        image_1 = gr.Image()
        image_2 = gr.Image()
        image_3 = gr.Image()
        image_4 = gr.Image()

    convert_button.click(convert_audio, inputs=[audio_window], outputs=[image_1, image_2, image_3, image_4])

demo.launch()
