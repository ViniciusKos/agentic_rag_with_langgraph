from typing import Dict, Any
from config import load_config
import pprint
from retriever.tools import setup_retriever
from agent.graph import create_workflow

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
    graph = create_workflow(agent_state=config, tools=tools)
    
    print("\nRAG Agentic initialized and ready to answer questions!")
    print("Type 'exit' to terminate the program.")

    while True:
        # Prompt the user for input
        question = input("\nEnter your question: ").strip()
        
        # Check if the user wants to exit
        if question.lower() in ['sair', 'exit', 'quit']:
            print("Exiting program...")
            break
        
        if not question:
            print("Please enter a valid question.")
            continue
        
        try:
            print("\nProcessing your question...")
            # Create the input and process through the graph
            inputs = create_input_message(question)
            
            # Process the question through the graph
            for output in graph.stream(inputs):
                process_output(output)
                
        except Exception as e:
            print(f"\nError processing the question: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()