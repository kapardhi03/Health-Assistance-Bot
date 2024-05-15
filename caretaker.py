import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    if "login_success" not in st.session_state:
        st.session_state.login_success = False

    if not st.session_state.login_success:
        with st.form("login_form"):
            st.header("CareTaker")
            patient_name = st.text_input("Patient Name")
            # password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")

            if login_button:
                if patient_name == "John" :
                    st.session_state.login_success = True  
                else:
                    st.error("Invalid patient name or password.")
    else:
        show_dashboard()

def show_dashboard():
    data = {
        "Appointments": [
            {
                "_id": 1,
                "Doctor": {
                    "name": "Dr. Smith",
                    "specialist": "Cardiology"
                },
                "Date": "2023-03-21",
                "status": "false"
            },
            {
                "_id": 2,
                "Doctor": {
                    "name": "Dr. Johnson",
                    "specialist": "Dermatology"
                },
                "Date": "2023-03-25",
                "status": "false"
            },
            {
                "_id": 3,
                "Doctor": {
                    "name": "Dr. Garcia",
                    "specialist": "Pediatrics"
                },
                "Date": "2023-03-28",
                "status": "true"
            },
            {
                "_id": 4,
                "Doctor": {
                    "name": "Dr. Lee",
                    "specialist": "Oncology"
                },
                "Date": "2023-04-02",
                "status": "true"
            },
            {
                "_id": 5,
                "Doctor": {
                    "name": "Dr. Martinez",
                    "specialist": "Neurology"
                },
                "Date": "2023-04-05",
                "status": "false"
            }
        ],
        "History": {
            "Appointments": {
                "Total appointments": 5
            },
            "medication_list": {
                "Medicines": [
                    {"paracetamol": 5},
                    {"Dolo": 2},
                    {"nothing65": 10}
                ]
            }
        },
        "Emergency": [
            {
                "_id": 1,
                "Date": "2023-03-21",
                "case": "Heart problem",
                "Doctor_consulted": "Dr. Smith"
            },
            {
                "_id": 2,
                "Date": "2023-03-23",
                "case": "Accident",
                "Doctor_consulted": "Dr. Johnson"
            }
        ],
    }

    st.header("Appointment Statistics")
    appointments = data["Appointments"]
    total_appointments = len(appointments)
    successful_appointments = sum(1 for appointment in appointments if appointment["status"]=="true")
    missed_appointments = total_appointments - successful_appointments

    appointment_stats = pd.DataFrame({
        "Status": ["Successful", "Missed"],
        "Count": [successful_appointments, missed_appointments]
    })
    fig = px.pie(appointment_stats, values="Count", names="Status", title="Appointment Status")
    st.plotly_chart(fig, use_container_width=True)

    st.header("Upcoming Appointments")
    for appointment in appointments:
        st.subheader(f"Appointment with {appointment['Doctor']['name']} ({appointment['Doctor']['specialist']})")
        st.write(f"Date: {appointment['Date']}")
        st.write(f"Status: {'Scheduled' if appointment['status'] else 'Missed'}")

    st.header("Appointment History")
    st.write(f"Total appointments: {data['History']['Appointments']['Total appointments']}")

    st.header("Medication List")
    medication_list = data["History"]["medication_list"]["Medicines"]
    for medicine in medication_list:
        for med, duration in medicine.items():
            st.write(f"{med}: {duration} days")

    st.header("Emergency Cases")
    for emergency in data["Emergency"]:
        st.subheader(f"Emergency Case ({emergency['Date']})")
        st.write(f"Case: {emergency['case']}")
        st.write(f"Doctor Consulted: {emergency['Doctor_consulted']}")

# Run the Streamlit app
if __name__ == "__main__":
    st.set_page_config(page_title="Caretaker Dashboard", page_icon=":guardsman:")
    main()