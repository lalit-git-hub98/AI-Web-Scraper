from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Define the template for the prompt
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Initialize the OpenAI model (GPT-4)
model = ChatOpenAI(model="gpt-4")

def parse_with_openai(dom_chunks, parse_description):
    # Create the prompt template
    prompt = ChatPromptTemplate.from_template(template)
    
    # Chain the prompt with the model using LLMChain
    chain = LLMChain(prompt=prompt, llm=model)

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        # Invoke the chain with the required parameters
        response = chain.run(dom_content=chunk, parse_description=parse_description)
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        
        parsed_results.append(response)

    # Join the parsed results as strings
    return "\n".join(parsed_results)
