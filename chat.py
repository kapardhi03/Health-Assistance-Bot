from openai import OpenAI
import json
from PharmEasy import searchPE
from Tata import searchTata
import main
import mongo_call

client = OpenAI(api_key="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")

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
        "description": "Books an appointment with a doctor when a doctor is selected, if Doctor, time and date is in context",
        "parameters": {
            "type": "object",
            "properties": {
                "doctor": {
                    "type": "string",
                    "description": "The name of the doctor you want appoitment with."
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
        "type": "function",
        "name": "give_doctors",
        "description": "Gives the list of doctors to select to the user when asked",
    },
    {
        "type": "function",
        "name": "add_medication",
        "description": "Add a medication schedule for a user.",
        "parameters": {
            "type": "object",
            "properties": {
                "medication_name": {
                    "type": "string",
                    "description": "The name of the medication.",
                },
                "time": {
                    "type": "string",
                    "description": "The time of day when the medication should be taken (e.g., '08:00 AM').",
                },
                "days": {
                    "type": "array",
                    "description": "The list of days on which the medication should be taken (e.g., ['Monday', 'Tuesday']).",
                    "items": {
                        "type": "string",
                        "enum": [
                            "Monday",
                            "Tuesday",
                            "Wednesday",
                            "Thursday",
                            "Friday",
                            "Saturday",
                            "Sunday",
                        ],
                    },
                    "minItems": 1,
                },
                "dosage": {
                    "type": "number",
                    "description": "The dosage or number of tablets to be taken.",
                },
                "until": {
                    "type": "string",
                    "description": "Specifies the duration for which the medication schedule should be followed (e.g., 'one month', 'one week', 'a day').",
                },
            },
            "required": ["user", "days", "time", "dosage", "medication_name", "until"],
        },
    },
    {
        "type": "function",
        "name": "emergency",
        "description": "This function is triggered when a user's message suggests an urgent situation or emergency, enabling appropriate actions or notifications."
    },
    {
        "type": "function",
        "name": "fetch_pricing",
        "description": "fetches the details of the medicine and when a medicine name is given",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "medicine name you want to buy"
                },
                
            },
            "required": ["name"]
        }
    },
    {
        "type": "function",
        "name": "get_appointments",
        "description": "This function retrieves the details of all available appointments from the system."
    }
]

def give_doctors():
    return {"task": "give_doctors", "data": doctors}

# def find_docs(location, specialization, date, time):
#     desired_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
#     closest_doctor_info = None
#     min_time_difference = timedelta.max

#     for doctor in doctors:
#         if doctor['location'].lower() == location.lower() and doctor['specialization'].lower() == specialization.lower():
#             for available_date, available_time in doctor['availability']:
#                 available_datetime = datetime.strptime(f"{available_date} {available_time}", "%Y-%m-%d %H:%M")
#                 time_difference = abs(available_datetime - desired_datetime)
                
#                 if time_difference < min_time_difference:
#                     closest_doctor_info = {
#                         "name": doctor['name'],
#                         "date": available_date,
#                         "time": available_time
#                     }
#                     min_time_difference = time_difference
    
#     if closest_doctor_info:
#         return {"status": True, "data": closest_doctor_info}
#     else:
#         return {"status": False, "data": "No doctors are available matching your criteria."}

def book_appointment(doctor, date, time, location, user):
    return_data = main.create_appointment(doctor=doctor,
                            date=date,
                            time=time,
                            user=user,
                            location=location)
    if return_data["status"] == True:
        print(f"booked with {doctor}, {date}, {time}, {location}")
        return {"task": "book_appointment", "data":{"status": True, "doctor": doctor, "date": date, "time": time, "location": location, "numerical": return_data["data"]}}
    else:
        return {"task": "book_appointment", "data":{"status": False, "message": "Error occured"}}

def add_medication(days, time, dosage, medication_name, until, user):
    return_data = main.add_medication(user=user,
                        days=days,
                        time=time,
                        dosage=dosage,
                        medication_name=medication_name,
                        untill=until)
    if return_data["status"] == True:
        print(f"added medication {medication_name} of dosage {dosage}, at {time} on {days}, for a {until} for {user}")
        return {"task": "add_medication", "data":{"status": True, "days": days, "time": time, "dosage": dosage,
                "medication_name": medication_name, "until": until}}
    else:
        return {"task": "add_medication", "data":{"status": False, "msg": "Error occured"}}

def emergency():
    print("Emergency is called")
    return {"task": "emergency", "data": "called emergency services"}

def fetch_pricing(name):
    sear_tata = searchTata(name=name)
    search_pe = searchPE(name=name)
    return {"task": "fetch_pricing", "data":{"message":"below are the prices", "options": [sear_tata, search_pe]}}

def get_appointments(user):
    return {"task": "get_appointments", "data": mongo_call.view_appointments(user=user)}

messages = [{"role": "system", "content": f"You are a medical assistant. \
             To help people you have the doctors informations: \
             {doctors}"}]

def do_chat():
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=function_descriptions,
            function_call="auto",
        )
        return response
    except Exception as e:
        print(e)
        return None

def chat(query, user):
    messages.append({"role": "user", "content": query})
    response = do_chat()
    while response is None:
        response = do_chat()

    if response.choices[0].finish_reason.lower() == "stop":
        return_data = {"task": "message", "data": response.choices[0].message.content}
        messages.append({"role": "assistant", "content": response.choices[0].message.content})

    elif response.choices[0].finish_reason.lower() == "function_call":

        if response.choices[0].message.function_call.name.lower() == "book_appointment":
            messages.append({"role": "assistant", "content": str(response.choices[0].message.function_call)})
            function_args = json.loads(response.choices[0].message.function_call.arguments)
            return_data = book_appointment(doctor=function_args["doctor"],
                             date=function_args["date"],
                             time=function_args["time"],
                             location=function_args["location"],
                             user=user)
            
        elif response.choices[0].message.function_call.name.lower() == "give_doctors":
            return_data = give_doctors()

        elif response.choices[0].message.function_call.name.lower() == "add_medication":
            messages.append({"role": "assistant", "content": str(response.choices[0].message.function_call)})
            function_args = json.loads(response.choices[0].message.function_call.arguments)
            return_data = add_medication(days=function_args["days"],
                           time=function_args["time"],
                           dosage=function_args["dosage"],
                           medication_name=function_args["medication_name"],
                           until=function_args["until"],
                           user=user)
        elif response.choices[0].message.function_call.name.lower() == "emergency":
            return_data = emergency()
        elif response.choices[0].message.function_call.name.lower() == "fetch_pricing":
            messages.append({"role": "assistant", "content": str(response.choices[0].message.function_call)})
            function_args = json.loads(response.choices[0].message.function_call.arguments)
            return_data = fetch_pricing(function_args['name'])

        elif response.choices[0].message.function_call.name.lower() == "get_appointments":
            return_data = get_appointments(user=user)

    return return_data
            
# if __name__ == "__main__":
#     while 1:
#         query = input()
#         chat(query, "abhinav")
