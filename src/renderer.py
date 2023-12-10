from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich.padding import Padding
from voice2image.main import voice_to_image
from real_time_translation.main import live_translate
import argparse

console = Console()
modes_list = ['voice', 'v', 'translate', 't']

choices_table = Table(
    show_header=True, 
    header_style="bold magenta"
)

choices_table.add_column(
    "Modes", 
    style="dim", 
    width=14
)
choices_table.add_column(
    "Descriptions", 
    width=45
)

choices_table.add_row(
    f"{modes_list[0]} ({modes_list[1]})", 
    "Convert voice prompt into beautiful images."
)
choices_table.add_row(
    f"{modes_list[2]} ({modes_list[3]})", 
    "Multi-lingual real-time audio translation." 
)

running_table = Table(show_header=False)
running_table.add_column(
    "Information", 
    justify="center"
)

def run_mode(mode, function):
    if function:
        running_table.add_row(f">>> Now running {read(mode)} <<<")
        vetical_padding()
        console.print(Align.left(running_table))
        vetical_padding()
        function()
    else:
        console.print(f"Error: Invalid mode - {mode}")
 
def read(mode_string):
    if mode_string.lower() in modes_list[:2]:
        return 'voice'
    if mode_string.lower() in modes_list[2:]:
        return 'translate'
    
def vetical_padding():
    console.print(Padding("", (0, 0)))

modes_mapped_to_functions = {
    modes_list[0]: voice_to_image, 
    modes_list[1]: voice_to_image, 
    modes_list[2]: live_translate,
    modes_list[3]: live_translate
}

modes_help_descriptions = {
    modes_list[0]: "Convert your voice into images",
    modes_list[1]: "Short form for 'voice'",
    modes_list[2]: "Get live translations",
    modes_list[3]: "Short form for 'translate'",
}

parser = argparse.ArgumentParser(
    prog='python src/main.py',
    description=(
        "\nThis app has 2 exciting functioning modes:"
        "\n   1. 'voice' or 'v'."
        "\n   2. 'translate' or 't'."
    ),
    formatter_class=argparse.RawDescriptionHelpFormatter
)

for mode, help_text in modes_help_descriptions.items():
    parser.add_argument(
        f'--{mode}', 
        action='store_const', 
        const=mode, 
        dest='mode', 
        help=help_text
    )