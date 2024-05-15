from datetime import datetime, timedelta

doctors = [
    {
        "name": "Dr.Smith",
        "location": "New York",
        "specialization": "Cardiology",
        "availability": [("2024-03-21", "10:00"), ("2024-03-22", "15:00")],
    },
    {
        "name": "Dr.Jones",
        "location": "Los Angeles",
        "specialization": "Dermatology",
        "availability": [("2024-03-21", "09:00"), ("2024-03-22", "14:00")],
    },
    {
        "name": "Dr.Lee",
        "location": "New York",
        "specialization": "Pediatrics",
        "availability": [("2024-03-21", "11:00"), ("2024-03-22", "16:00")],
    },
    {
        "name": "Dr.Kim",
        "location": "Los Angeles",
        "specialization": "Cardiology",
        "availability": [("2024-03-21", "10:00"), ("2024-03-22", "15:00")],
    },
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
                    "description": "The name of the doctor you want appoitment with.",
                },
                "location": {
                    "type": "string",
                    "description": "The location where the user wants to find a doctor.",
                },
                "date": {
                    "type": "string",
                    "description": "The desired date for the appointment in the format 'YYYY-MM-DD'.",
                },
                "time": {
                    "type": "string",
                    "description": "The desired time for the appointment in the format 'HH:MM'.",
                },
            },
            "required": ["doctor", "location", "date", "time"],
        },
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
                "time": {
                    "type": "string",
                    "description": "The time of day when the medication should be taken (e.g., '08:00 AM').",
                },
                "dosage": {
                    "type": "number",
                    "description": "The dosage or number of tablets to be taken.",
                },
                "medication_name": {
                    "type": "string",
                    "description": "The name of the medication.",
                },
                "until": {
                    "type": "string",
                    "description": "Specifies the duration for which the medication schedule should be followed (e.g., 'one month', 'one week', 'a day').",
                },
            },
            "required": ["user", "days", "time", "dosage", "medication_name", "until"],
        },
    },
]


def find_docs(location, specialization, date, time):
    desired_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    closest_doctor_info = None
    min_time_difference = timedelta.max

    for doctor in doctors:
        if (
            doctor["location"].lower() == location.lower()
            and doctor["specialization"].lower() == specialization.lower()
        ):
            for available_date, available_time in doctor["availability"]:
                available_datetime = datetime.strptime(
                    f"{available_date} {available_time}", "%Y-%m-%d %H:%M"
                )
                time_difference = abs(available_datetime - desired_datetime)

                if time_difference < min_time_difference:
                    closest_doctor_info = {
                        "name": doctor["name"],
                        "date": available_date,
                        "time": available_time,
                    }
                    min_time_difference = time_difference

    if closest_doctor_info:
        return {"status": True, "data": closest_doctor_info}
    else:
        return {
            "status": False,
            "data": "No doctors are available matching your criteria.",
        }


def book_appointment(doctor, date, time, location, user):
    print(f"booked with {doctor}, {date}, {time}, {location} for {user}")



