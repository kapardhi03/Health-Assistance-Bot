import os
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

from openai import OpenAI


client = OpenAI(api_key="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")

Doctor = Dict[str, str]
Availability = List[Tuple[str, str]]

doctors: List[Dict[str, str | Availability]] = [
    {'name': 'Dr. Smith', 'location': 'New York', 'specialization': 'Cardiology',
     'availability': [('2024-03-21', '10:00'), ('2024-03-22', '15:00')]},
    {'name': 'Dr. Jones', 'location': 'Los Angeles', 'specialization': 'Dermatology',
     'availability': [('2024-03-21', '09:00'), ('2024-03-22', '14:00')]},
    {'name': 'Dr. Lee', 'location': 'New York', 'specialization': 'Pediatrics',
     'availability': [('2024-03-21', '11:00'), ('2024-03-22', '16:00')]},
    {'name': 'Dr. Kim', 'location': 'Los Angeles', 'specialization': 'Cardiology',
     'availability': [('2024-03-21', '10:00'), ('2024-03-22', '15:00')]},
]

function_descriptions = [
    {
        "type": "function",
        "name": "book_appointment",
        "description": "Books an appointment with a doctor when a doctor is selected",
        "parameters": {
            "type": "object",
            "properties": {
                "doctor": {
                    "type": "string",
                    "description": "The name of the doctor you want an appointment with."
                },
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
            "required": ["doctor", "location", "date", "time"]
        }
    },
    {
        "name": "find_docs",
        "description": "Gives the list of doctors to select from",
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
    {
        "name": "add_medication",
        "description": "Add a medication schedule for a user.",
        "parameters": {
            "type": "object",
            "properties": {
                "user": {
                    "type": "string",
                    "description": "The username of the user for whom the medication schedule is being added."
                },
                "days": {
                    "type": "array",
                    "description": "The list of days on which the medication should be taken (e.g., ['Monday', 'Tuesday']).",
                    "items": {
                        "type": "string",
                        "enum": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                    },
                    "minItems": 1
                },
                "time": {
                    "type": "string",
                    "description": "The time of day when the medication should be taken (e.g., '08:00 AM')."
                },
                "dosage": {
                    "type": "number",
                    "description": "The dosage or number of tablets to be taken."
                },
                "medication_name": {
                    "type": "string",
                    "description": "The name of the medication."
                },
                "until": {
                    "type": "string",
                    "description": "Specifies the duration for which the medication schedule should be followed (e.g., 'one month', 'one week', 'a day')."
                }
            },
            "required": ["user", "days", "time", "dosage", "medication_name", "until"]
        }
    }
]

def find_docs(location: str, specialization: str, date: str, time: str) -> Dict[str, bool | List[Dict[str, str | List[Dict[str, str]]]]]:
    """
    Find doctors matching the given criteria and return their availability.

    Args:
        location (str): The location where doctors are being searched for.
        specialization (str): The specialization of the doctor being searched for.
        date (str): The date for which doctors are being searched.
        time (str): The time at which doctors are being searched.

    Returns:
        Dict[str, bool | List[Dict[str, str | List[Dict[str, str]]]]]: A dictionary containing the status (True or False)
        and the data, which is either a list of available doctors with their available slots or an error message.
    """
    desired_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    available_doctors = []

    for doctor in doctors:
        if doctor['location'].lower() == location.lower() and doctor['specialization'].lower() == specialization.lower():
            doctor_available_slots = []
            for available_date, available_time in doctor['availability']:
                available_datetime = datetime.strptime(f"{available_date} {available_time}", "%Y-%m-%d %H:%M")
                time_difference = abs(available_datetime - desired_datetime)

                if time_difference <= timedelta(days=1):  # Consider slots within 1 day range
                    doctor_available_slots.append({
                        "date": available_date,
                        "time": available_time
                    })

            if doctor_available_slots:
                available_doctors.append({
                    "name": doctor['name'],
                    "available_slots": doctor_available_slots
                })

    if available_doctors:
        return {"status": True, "data": available_doctors}
    else:
        return {"status": False, "data": "No doctors are available matching your criteria."}

def book_appointment(doctor: str, date: str, time: str, location: str, user: str):
    """
    Book an appointment with a doctor at a specific date, time, and location for a given user.

    Args:
        doctor (str): The name of the doctor for the appointment.
        date (str): The date for the appointment in the format 'YYYY-MM-DD'.
        time (str): The time for the appointment in the format 'HH:MM'.
        location (str): The location where the appointment will take place.
        user (str): The username of the user booking the appointment.
    """
    # Implement the logic to book the appointment for the given user
    print(f"Booked appointment with {doctor} on {date} at {time} in {location} for {user}")

def add_medication(user: str, days: List[str], time: str, dosage: float, medication_name: str, until: str):
    """
    Add a medication schedule for a user.

    Args:
        user (str): The username of the user for whom the medication schedule is being added.
        days (List[str]): The list of days on which the medication should be taken (e.g., ['Monday', 'Tuesday']).
        time (str): The time of day when the medication should be taken (e.g., '08:00 AM').
        dosage (float): The dosage or number of tablets to be taken.
        medication_name (str): The name of the medication.
        until (str): Specifies the duration for which the medication schedule should be followed (e.g., 'one month', 'one week', 'a day').
    """
    # Implement the logic to add the medication schedule for the given user
    print(f"Added medication '{medication_name}' with dosage {dosage}, at {time} on {', '.join(days)}, for {until} for {user}")

messages = [{"role": "system", "content": f"You are a medical assistant. \
             To help people you have the doctors information: \
             {doctors}"}]

def do_chat():
    """
    Create a chat completion using the OpenAI API and return the response.

    Returns:
        The response object from the OpenAI API, or None if an exception occurred.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=messages,
            functions=function_descriptions,
            function_call="auto",
        )
        return response
    except Exception as e:
        print(e)
        return None

def chat(query: str, user: str):
    """
    Handle the user's query and perform the appropriate action based on the response from the OpenAI API.

    Args:
        query (str): The user's query or request.
        user (str): The username of the user making the request.
    """
    messages.append({"role": "user", "content": query})
    response = do_chat()
    while response is None:
        response = do_chat()

    if response.choices[0].finish_reason.lower() == "stop":
        print(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": response.choices[0].message.content})
    elif response.choices[0].finish_reason.lower() == "function_call":
        if response.choices[0].message.function_call.name.lower() == "book_appointment":
            function_args = json.loads(response.choices[0].message.function_call.arguments)
            book_appointment(doctor=function_args["doctor"],
                             date=function_args["date"],
                             time=function_args["time"],
                             location=function_args["location"],
                             user=user)

        elif response.choices[0].message.function_call.name.lower() == "find_docs":
            function_args = json.loads(response.choices[0].message.function_call.arguments)
            docs = find_docs(specialization=function_args["specialization"],
                             date=function_args["date"],
                             location=function_args["location"],
                             time=function_args["time"])
            if docs["status"]:
                print("Available doctors:")
                for doctor in docs["data"]:
                    print(f"{doctor['name']}")
                    print("Available slots:")
                    for slot in doctor["available_slots"]:
                        print(f"   {slot['date']} at {slot['time']}")

        elif response.choices[0].message.function_call.name.lower() == "add_medication":
            function_args = json.loads(response.choices[0].message.function_call.arguments)
            add_medication(user=user,
                           days=function_args["days"],
                           time=function_args["time"],
                           dosage=function_args["dosage"],
                           medication_name=function_args["medication_name"],
                           until=function_args["until"])

if __name__ == "__main__":
    while True:
        query = input("Enter your request: ")
        user = input("Enter your username: ")
        chat(query, user)