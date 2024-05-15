import mongo
import uuid

'''
CFU:could not find user
CFA: could not find appointment with given query
MFU : medcine not found
'''
def view_appointments(user):
    return mongo.fetch_documents("app","appointments",{user:{"$exists":True}})['data'][0][user]


def add_appointment(doctor,date,time,user,location):
    doc=mongo.fetch_documents("app","appointments",{user:{"$exists":True}})['data']
    if(len(doc)==0):
        mongo.insert_document("app","appointments", {user : [{"Date":date,"Doctor":doctor,"Time":time,"Location":location,"attended":"Pending"}]})
    else:
        doc=doc[0]
        doc[user].append({"Date":date,"Doctor":doctor,"Time":time,"Location":location,"attended":"Pending"})
        delete_status=mongo.delete_document("app","appointments",{user:{"$exists":True}})
        if delete_status['status']:
            return{"status":mongo.insert_document("app","appointments",doc)['status'],"error":""}

# add_appointment("mr doc1","today1","now1","kapardhi","earth1")
            
def set_visited(user,doctor,time,date):
    doc=mongo.fetch_documents("app","appointments",{user:{"$exists":True}})['data']
    if(len(doc)==0):
        return{"status":False,"error":"CFU"}
    else:
        doc=doc[0]
        modified=False
        for a in doc[user]:
            if(a['Doctor']==doctor):
                a['attended']="attended"
                modified=True
        if not modified: return{"status":False,"error":"Could not find such an appointment"}
        delete_status=mongo.delete_document("app","appointments",{user:{"$exists":True}})
        if delete_status['status']:
            return{"status":mongo.insert_document("app","appointments",doc)['status'],"error":""}

        

# set_visited("kapardhi","mr doc1","now1","today1")

def add_medication(user,days,time,dosage,medication_name,untill):
    doc=mongo.fetch_documents("app","medications",{user:{"$exists":True}})['data']
    if(len(doc)==0):
        mongo.insert_document("app","medications", 
            {user:
                [{"medication_name":medication_name,"Days":days, "time":time, "dosage":dosage, "untill":untill}]
            }
        )
    else:
        doc=doc[0]
        doc[user].append({"medication_name":medication_name,"Days":days, "time":time, "dosage":dosage, "untill":untill})
        delete_status=mongo.delete_document("app","medications",{user:{"$exists":True}})
        if delete_status['status']:
            return{"status":mongo.insert_document("app","medications",doc)['status'],"error":""}

# add_medication("kapardhi",["Tuesday","Wednesday"],"10:00","1","X","December")
        
def insert_num(num,params):
    return mongo.insert_document("app","hashmap",{num:params})

def get_object(num):
    return(mongo.fetch_documents("app","hashmap",{num:{"$exists":True}}))['data'][0][num]

def insert_med_logs(med_numerical):
    mongo.insert_document("app","consumptions",{med_numerical:False})

def set_met_logs(numerical):
    doc=mongo.fetch_documents("app","consumptions",{numerical:{"$exists":True}})['data']
    if(len(doc)==0):
        return{"status":False,"error":"MFU"}
    else:
        doc=doc[0]
        doc[numerical]=True
        delete_status=mongo.delete_document("app","consumptions",{numerical:{"$exists":True}})
        if delete_status['status']:
            return{"status":mongo.insert_document("app","consumptions",doc)['status'],"error":""}

    
def emergency(user, date):
    mongo.insert_document("app","emergency",{user:date})