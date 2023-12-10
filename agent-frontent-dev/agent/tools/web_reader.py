

from typing import Any, Dict
import requests

def read_webpage(url: str) -> str:
    """Read the html of the given url and return it in a string.

    Args:
        url (str): The url you want to read the page from

    Returns:
        str: The html content of the webpage as a string, or a meaningful error message.
    """
    try:
        response = requests.get(url)
        return response.text
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {str(e)}"


class WebPageToolExecutor:
    function_names = ["readWebpage"]
    def run(self, function_name: str, **parameters: Dict[str, Any]) -> Any:
        """This method should be implemented by the tool. 
        It should contain the logic to run the tool.
        """
        if function_name == "readWebpage":
            return read_webpage(**parameters)
        raise NotImplementedError
    
    @staticmethod
    def support(function_name: str) -> bool:
        """This method should be implemented by the tool. 
        It should return True if the tool supports the given function_name.
        """
        if function_name in WebPageToolExecutor.function_names:
            return True
        return False


def get_tools() -> list:
    """Get a list the function in this file.

    Returns:
        list: A list of all the tools in this file.
    """
    tools = [
         {
            "type": "function",
            "function": {
                "name": "readWebpage",
                "description": "Read the html of the given url and return it in a string.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string", 
                            "description": "The url you want to read the page from"
                        },
                    },
                    "required": ["url"]
                }
            }
        }, 
    ]
    return tools


if __name__ == "__main__":
    print(read_webpage("https://www.google.com"))