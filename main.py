import mongo_call
import uuid

def create_numerical(params):
    return str(uuid.uuid4())

def create_appointment(doctor, date, time, user,location):
    numerical=create_numerical([doctor,date,time,user,location])
    mongo_call.insert_num(numerical,[doctor,date,time,user,location])
    mongo_call.add_appointment(doctor,date,time,user,location)
    return{"status":True,"data":numerical}

def set_visited(numerical):
    doctor,date,time,user,location=mongo_call.get_object(numerical)
    mongo_call.set_visited(user,doctor,time,date)
    return{"status":True}

def add_medication(user,days,time,dosage,medication_name,untill):
    numerical=create_numerical([user,days,time,dosage,medication_name,untill])
    mongo_call.insert_num(numerical,[user,days,time,dosage,medication_name,untill])
    mongo_call.add_medication(user,days,time,dosage,medication_name,untill)
    med_numericals=[]
    for day in days:
        med_numerical=create_numerical("")
        med_numericals.append(med_numerical)
        mongo_call.insert_med_logs(med_numerical)
    return{"status":True,"data":f"medication {numerical} consumption{med_numericals}"}

def view_appointments(user):
    mongo_call.view_appointments(user)

def consumed_medicine(numerical):
    mongo_call.set_met_logs(numerical)

def emergency(user,date):
    mongo_call.emergency(user,date)

# emergency("kap","12-03-2032")
# consumed_medicine("68b8c719-1b64-47f8-bc7f-2e6d22210fdd")
#print(add_medication("kapardhi",["Saturday"],"10:00","1","DX", "December"))
#print(create_appointment("doc2","today","now","kapardhi","here"))
#print(set_visited("babbfbec-9557-4200-b60b-87652db25c42"))