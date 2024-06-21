
from llama_index.readers import SimpleWebPageReader
from llama_index import VectorStoreIndex
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main(url: str) -> None:
    # Load the web page content
    document = SimpleWebPageReader(html_to_text=True).load_data(urls=[url])
    
    # Create a vector store index from the document
    index = VectorStoreIndex.from_documents(documents=document)
    
    # Convert the index into a query engine
    query_engine = index.as_query_engine()
    
    # Query the engine for information about the history of generative AI
    response = query_engine.query("what is the history of generative ai?")
    
    # Print the response to the console
    print(response)

# If this script is run as the main module, execute the main function
if __name__ == "__main__":
    main(url="https://medium.com/@social_65128/the-comprehensive-guide-to-understanding-generative-ai-c06bbf259786")
