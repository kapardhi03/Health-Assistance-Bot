from openai import OpenAI
import json
from datetime import datetime, timedelta

client = OpenAI(
    api_key="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"
)

doctors = [
    {'name': 'Dr. Smith', 'location': 'New York', 'specialization': 'Cardiology', 'availability': [('2024-03-21', '10:00'), ('2024-03-22', '15:00')]},
    {'name': 'Dr. Jones', 'location': 'Los Angeles', 'specialization': 'Dermatology', 'availability': [('2024-03-21', '09:00'), ('2024-03-22', '14:00')]},
    {'name': 'Dr. Lee', 'location': 'New York', 'specialization': 'Pediatrics', 'availability': [('2024-03-21', '11:00'), ('2024-03-22', '16:00')]},
    {'name': 'Dr. Kim', 'location': 'Los Angeles', 'specialization': 'Cardiology', 'availability': [('2024-03-21', '10:00'), ('2024-03-22', '15:00')]},
]

function_descriptions = [
    {
        "type": "function",
        "name": "book_appointment",
        "description": "Books an appointment for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location where the user wants to find a doctor."
                },
                "date": {
                    "type": "string",
                    "description": "The desired date for the appointment in the format 'YYYY-MM-DD'."
                },
                "time": {
                    "type": "string",
                    "description": "The desired time for the appointment in the format 'HH:MM'."
                }
            },
            "required": ["location", "date", "time"]
        }
    },
      {
        "name": "find_docs",
        "description": "Gives the list of doctors",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location where doctors are being searched for",
                },
                "date": {
                    "type": "string",
                    "description": "The date for which doctors are being searched",
                },
                "time": {
                    "type": "string",
                    "description": "The time at which doctors are being searched",
                },
                "specialization": {
                    "type": "string",
                    "description": "The specialization of the doctor being searched for",
                },
            },
            "required": ["location", "date", "time", "specialization"],
        },
    },
]

def find_docs(location, specialization, date, time):
    desired_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    closest_doctor_info = None
    min_time_difference = timedelta.max

    for doctor in doctors:
        if doctor['location'].lower() == location.lower() and doctor['specialization'].lower() == specialization.lower():
            for available_date, available_time in doctor['availability']:
                available_datetime = datetime.strptime(f"{available_date} {available_time}", "%Y-%m-%d %H:%M")
                time_difference = abs(available_datetime - desired_datetime)
                
                if time_difference < min_time_difference:
                    closest_doctor_info = {
                        "name": doctor['name'],
                        "date": available_date,
                        "time": available_time
                    }
                    min_time_difference = time_difference
    
    if closest_doctor_info:
        return {"status": True, "data": closest_doctor_info}
    else:
        return {"status": False, "data": "No doctors are available matching your criteria."}

def book_appointment(date, time, location):
    print("booked")

messages = [{"role": "system", "content": "You are a medical assistant"}]

def do_chat():
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            functions=function_descriptions,
            function_call="auto",
        )
        return response
    except Exception as e:
        print(e)
        return None

def chat(query):
    messages.append({"role": "user", "content": query})
    response = do_chat()
    while response is None:
        response = do_chat()

    if response.choices[0].finish_reason.lower() == "stop":
        print(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": response.choices[0].message.content})
    elif response.choices[0].finish_reason.lower() == "function_call":
        # messages.append({"role": "assistant", "content": str(response.choices[0].message.function_call)})

        if response.choices[0].message.function_call.name.lower() == "book_appointment":
            function_args = json.loads(response.choices[0].message.function_call.arguments)
            book_appointment(date=function_args["date"],
                             time=function_args["time"],
                             location=function_args["location"])
            
        elif response.choices[0].message.function_call.name.lower() == "find_docs":
            function_args = json.loads(response.choices[0].message.function_call.arguments)
            docs = find_docs(specialization=function_args["specialization"],
                      date=function_args["date"],
                      location=function_args["location"],
                      time=function_args["time"])
            print(docs)


if _name_ == "_main_":
    while 1:
        query = input()
        chat(query)

# I need to book an appointment with a cardiologist at 10am on 21st march