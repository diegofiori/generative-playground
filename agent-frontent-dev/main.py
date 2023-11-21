from agent.agents import FrontendAgentRunner


def _main_loop(agent: FrontendAgentRunner):
    input_text = input("Enter your request: ")
    assistant_messages = agent.run(input_text)
    for message in assistant_messages:
        print(f"{message.role}: {message.content}")
    
    


def main():
    agent = FrontendAgentRunner()
    while True:
        try:
            _main_loop(agent)
        except KeyboardInterrupt:
            print("Interrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")