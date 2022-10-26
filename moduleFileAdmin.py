from http import client
import streamlit as st
from datetime import datetime, date, time
import firebase_admin
from firebase_admin import credentials, firestore

fileName = str(date.today())
fileName = fileName + ".csv"

if not firebase_admin._apps:
    cred = credentials.Certificate("certificate.json")
    app = firebase_admin.initialize_app(cred)

store = firestore.client()

collection_name = fileName

doctorFileName = "DoctorList.csv"
clientFileName = "ClientList.csv"
settingFileName = "Setting.csv"

def deleteData(type):
    docs = store.collection(collection_name).get()
    if type == "All":
        for doc in docs:
            key = doc.id
            store.collection(collection_name).document(key).delete()
    else:
        for doc in docs:
            if doc.id == type:
                store.collection(collection_name).document(doc.id).delete()
                break

def deleteDoctor(type):
    docs = store.collection(doctorFileName).get()
    if type == "All":
        for doc in docs:
            key = doc.id
            store.collection(doctorFileName).document(key).delete()
    else:
        for doc in docs:
            if doc.id == type:
                store.collection(doctorFileName).document(doc.id).delete()
                break

def deleteClient(type):
    docs = store.collection(clientFileName).get()
    if type == "All":
        for doc in docs:
            key = doc.id
            store.collection(clientFileName).document(key).delete()
    else:
        for doc in docs:
            if doc.id == type:
                store.collection(clientFileName).document(doc.id).delete()
                break

def uploadData(data, naming):
    store.collection(collection_name).document(naming).set(data)

def retriveData(type):
    data = []

    docs = store.collection(collection_name).get()
    for doc in docs:
        data.append(doc.to_dict())

    if type == "ID":
        IDs = []
        for each in data:
            IDs.append(each["Queue ID"])
        return IDs
    elif type == "All":
        return data
    else:
        for each in data:
            if (type == each["Queue ID"]):
                return each["Status"]

def updateData(QueueID, newStatus):
    docs = store.collection(collection_name).get()
    for doc in docs:
        key = doc.id
        temp = doc.to_dict()
        if QueueID == temp["Queue ID"]:
            store.collection(collection_name).document(key).update({"Status":newStatus})
            break

def uploadDoctor(doctor, naming):
    store.collection(doctorFileName).document(naming).set(doctor)

def retriveDoctor(caller):
    data = []

    docs = store.collection(doctorFileName).get()
    for doc in docs:
        data.append(doc.to_dict())

    if caller == "client":
        doctorNames = []
        for each in data:
            doctorNames.append(each["Doctor Name"])
        return doctorNames
    elif caller == "doctor":
        doctorInfo = []
        for each in data:
            doctorInfo.append([each["Doctor Name"], each["Password"]])
        return doctorInfo

def retrivePatients(doctor):
    data = retriveData("All")
    subData = []
    for each in data:
        if each["Doctor Name"] == doctor or each["Doctor Name"] == "Walk in":
            subData.append(each["Queue ID"])
    return subData

def uploadClient(doctor, naming):
    store.collection(clientFileName).document(naming).set(doctor)

def retriveClient():
    data = []

    docs = store.collection(clientFileName).get()
    for doc in docs:
        data.append(doc.to_dict())

    naming = []
    for each in data:
        naming.append(each["Client Name"])
    return naming

# ---------------------------------------------------------------------------------

if "Approved" not in st.session_state:
    st.session_state.Approved = False

st.title("Welcome To Admin Page, please Log in")

adminForm = st.form("adminInitialForm", clear_on_submit=True)
username = adminForm.text_input("Username")
password = adminForm.text_input("Password")
loginButton = adminForm.form_submit_button("Log in")

if loginButton:
    if username == "Admin" and password == "adminpass":
        st.session_state.Approved = True
        st.success("Log in successfully")
    else:
        st.error("Either wrong username or wrong password")

clientForm = st.form("clientDeleteForm", clear_on_submit=True)
clientName = clientForm.selectbox("Client Name", retriveClient())
clientSubmit = clientForm.form_submit_button("Delete Client Account")

if clientSubmit:
    if st.session_state:
        deleteClient(clientName)
    else:
        st.error("No access")

if st.button("Clear All Clients Account"):
    if st.session_state:
        deleteClient("All")
    else:
        st.error("No access")

queueForm = st.form("queueDeleteForm", clear_on_submit=True)
queueName = queueForm.selectbox("Queue ID", retriveData("ID"))
queueSubmit = queueForm.form_submit_button("Delete Queue")

if queueSubmit:
    if st.session_state:
        deleteData(queueName)
    else:
        st.error("No access")

if st.button("Clear All Queue"):
    if st.session_state:
        deleteData("All")
    else:
        st.error("No access")

doctorForm = st.form("doctorDeleteForm", clear_on_submit=True)
doctorName = doctorForm.selectbox("Doctor Name", retriveDoctor("client"))
doctorSubmit = doctorForm.form_submit_button("Delete Doctor Account")

if doctorSubmit:
    if st.session_state:
        deleteDoctor(doctorName)
    else:
        st.error("No access")

if st.button("Clear All Doctors Account"):
    if st.session_state:
        deleteDoctor("All")
    else:
        st.error("No access")