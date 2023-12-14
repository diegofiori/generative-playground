from functools import partial
import gradio as gr
from PIL import Image
from agent.agents import FrontendAgentRunner

def _main_loop(agent: FrontendAgentRunner, input_text: str, image: Image.Image = None):
    assistant_messages = agent.run(input_text, image=image)
    return "\n".join([f"{message.role}: {message.content}" for message in assistant_messages])

def main():
    agent = FrontendAgentRunner(verbose=True)
    _main_loop_with_agent = partial(_main_loop, agent)
    inputs = [
        gr.Textbox(lines=2, placeholder="Enter your request here..."),
        gr.Image(type="pil", label="Upload Image"),
    ]
    outputs = gr.Textbox()
    interface = gr.Interface(fn=_main_loop_with_agent, inputs=inputs, outputs=outputs)
    interface.launch()

if __name__ == "__main__":
    main()