import os
import gradio as gr

from ai_translate.models import (
    WhisperModel, TranslationModel, TextToVoice
)

debug = True
whisper_model = WhisperModel("whisper-1", verbose=debug)
translation_model = TranslationModel(verbose=debug)
voice_generation_model = TextToVoice(verbose=debug)


def translate_audio(audio_file, language):
    os.rename(audio_file, audio_file + '.wav')
    transcript = whisper_model(audio_file + '.wav')
    prompt = translation_model(transcript, language)
    path_to_voice = voice_generation_model(prompt, language)
    return path_to_voice


with gr.Blocks() as demo:
    # Add a title
    gr.Markdown(
        "# 🚀AI Translation🚀\n\nThe AI Translation app allows you to "
        "translate audio files into english and then read back the text "
        "to the user.\n\nEnjoy!🔥"
    )
    with gr.Row():
        audio_window = gr.Audio(
            sources="microphone", type="filepath", label="Input Audio"
        )
        language_dropdown = gr.Dropdown(
            label="Language", choices=["english", "spanish", "french"]
        )
    convert_button = gr.Button("Translate")
    with gr.Row():
        audio_out = gr.Audio(type="filepath", label="Input Audio")

    convert_button.click(
        translate_audio,
        inputs=[audio_window, language_dropdown],
        outputs=[audio_out]
    )

demo.launch()
