from typing import Dict, Any
from config import load_config
import pprint
from retriever.tools import setup_retriever

def initialize_environment() -> Dict[str, Any]:
    return load_config()

def create_input_message(question: str) -> Dict[str, list]:
    """Create the input message in the format expected by the graph"""
    return {
        "messages": [
            ("user", question),
        ]
    }

def process_output(output: Dict[str, Any]) -> None:
    """Process and display the graph output"""
    for key, value in output.items():
        print(f"\nOutput of node '{key}':")
        print("-" * 50)
        pprint.pprint(value, indent=2, width=80, depth=None)
        print("-" * 50)

def main():
    config = initialize_environment()
    print("Configurations loaded:")

    # Set up the retriever and the tools

    retriever_tool = setup_retriever()
    tools = [retriever_tool]
    
    # create the workflow

    