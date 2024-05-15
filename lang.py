from langchain.prompts import PromptTemplate
from langchain.agents import create_openai_functions_agent
from langchain_openai import ChatOpenAI

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
        {"name": "Dr. Williams", "specification": "Dentist"}
    ]
    filtered_docs = [doc for doc in available_docs if doc["specification"].lower() == specification.lower()]
    return filtered_docs[:3]  # Return at most 3 available doctors

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0,openai_api_key="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")


prompt = PromptTemplate(
    input_variables=["input"],
    output_variables=["agent_scratchpad"],
    template="You are an AI assistant that helps book medical appointments based on the user's input. You have access to the following tools: {tools}. Use these tools to accomplish the task of booking an appointment for the user. The input is: {input}"
)


# Create a list of tools
tools = [find_docs, book_appointment]

# Create an OpenAI Functions Agent
agent = create_openai_functions_agent(llm, tools, prompt)

# Define a custom AgentExecutor
class CustomAgentExecutor:
    def __init__(self, agent, tools, verbose=False):
        self.agent = agent
        self.tools = tools
        self.verbose = verbose

    def invoke(self, inputs):
        if self.verbose:
            print("User Input:", inputs["input"])
        response = self.agent.process(inputs["input"])
        if self.verbose:
            print("Agent Response:", response)

# Create an agent executor
agent_executor = CustomAgentExecutor(agent=agent, tools=tools, verbose=True)

# Invoke the agent
user_input = "I want to book an appointment with a cardiologist"
agent_executor.invoke({"input": user_input})
