import gradio as gr
from PIL import Image
from agent.agents import FrontendAgentRunner

def _main_loop(input_text: str, image: Image.Image = None):
    agent = FrontendAgentRunner()
    assistant_messages = agent.run(input_text, image=image)
    return "\n".join([f"{message.role}: {message.content}" for message in assistant_messages])

def main():
    inputs = [
        gr.Textbox(lines=2, placeholder="Enter your request here..."),
        gr.Image(type="pil", label="Upload Image"),
    ]
    outputs = gr.Textbox()
    interface = gr.Interface(fn=_main_loop, inputs=inputs, outputs=outputs)
    interface.launch()

if __name__ == "__main__":
    main()