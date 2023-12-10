import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))
from renderer import (
    run_mode, 
    choices_table, 
    console, 
    modes_mapped_to_functions, 
    vetical_padding, 
    parser
)

args = parser.parse_args()

def main():
    try:
        if args.mode:
            run_mode(
                args.mode.capitalize(), 
                modes_mapped_to_functions.get(args.mode)
            )
        else:
            vetical_padding()
            console.print(choices_table)
            while True:
                mode = input("\nPlease enter your mode choice: ")
                func = modes_mapped_to_functions.get(mode)
                if func:
                    run_mode(
                        mode.capitalize(), 
                        func
                    )
                    break
                else:
                    console.print(
                        "\n>>> Invalid choice <<<\n\nEnter either",
                        "'v' for 'voice' or 't' for 'translate'."
                    )
    except KeyboardInterrupt:
        console.print("\n\n>>> App closed <<<\n\n")
        sys.exit(0)
    except Exception as error:
        console.print(f"Error: {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()