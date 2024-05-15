from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.output_parsers import RegexOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.llms import ChatOpenAI
from langchain.agents import PythonCallbackManager
from langchain.output_parsers import RetryOutputParser as RegexOutputParser


# Define functions
def book_appointment(doc_name: str, date: str, time: str, specification: str):
    # Your logic to book an appointment
    print(f"Booking an appointment with {doc_name} ({specification}) on {date} at {time}")
    # Replace this with your actual logic for booking an appointment

def find_docs(location: str, date: str, time: str, specification: str):
    # Your logic to find available doctors based on the given criteria
    available_docs = [
        {"name": "Dr. Smith", "specification": "Cardiologist"},
        {"name": "Dr. Johnson", "specification": "Cardiologist"},
        {"name": "Dr. Williams", "specification": "Cardiologist"}
    ]
    filtered_docs = [doc for doc in available_docs if doc["specification"].lower() == specification.lower()]
    return filtered_docs[:3]  # Return at most 3 available doctors

# Define a prompt template for extracting parameters
param_extract_template = PromptTemplate(
    input_variables=["input", "required_params"],
    template="Extract the following parameters from the input: {required_params}",
)

# Define an output parser to parse the extracted parameters
param_extract_output_parser = RegexOutputParser.from_regex(r"(\w+)\s*:\s*(\w+)")

# Create a conversation chain with the language model and memory
memory = ConversationBufferMemory()
llm = ChatOpenAI()
conversation = ConversationChain(llm=llm, memory=memory)

# Create a Python callback manager
manager = PythonCallbackManager([book_appointment, find_docs])

# Handle user input
user_input = "I want to book an appointment with cardiologist"
result = conversation.predict(input=user_input)

# Classify intent
intent = None
if "book_appointment" in result.lower():
    intent = "book_appointment"
elif "find_doctors" in result.lower():
    intent = "find_doctors"

if intent == "book_appointment":
    # Extract parameters
    required_params = ["specification", "date", "time"]
    param_extract_prompt = param_extract_template.format(input=result, required_params=", ".join(required_params))
    param_extract_result = llm(param_extract_prompt)
    extracted_params = param_extract_output_parser.parse(param_extract_result)

    # Call book_appointment function with available parameters
    missing_params = [param for param in required_params if param not in extracted_params]
    if missing_params:
        # Call find_docs function
        available_docs = manager.call(find_docs, location="New York", date="2023-06-01", time="10:00 AM", specification=extracted_params.get("specification", ""))

        # Ask user to select a doctor and provide missing parameters
        print("Available doctors:")
        for i, doc in enumerate(available_docs):
            print(f"{i + 1}. {doc['name']} ({doc['specification']})")

        doc_choice = int(input("Select a doctor (1-3): ")) - 1
        extracted_params["doc_name"] = available_docs[doc_choice]["name"]
        date_str = input("Enter the date (YYYY-MM-DD): ")
        time_str = input("Enter the time (HH:MM AM/PM): ")
        extracted_params["date"] = date_str
        extracted_params["time"] = time_str

    # Call book_appointment function with complete parameters
    manager.call(book_appointment, **extracted_params)
else:
    print("Sorry, I didn't understand your request.")