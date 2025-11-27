import streamlit as st
from datetime import datetime, date
from api import (
    create_user,
    create_patient,
    create_appointment,
    get_patient_appointments,
    add_vitals,
    get_vitals,
    get_admin_stats,
    get_all_users,
    get_all_appointments,
    get_all_vitals,
    get_doctor_appointments,
    get_doctor_patients,
    create_diagnosis,
    get_doctor_diagnoses,
    create_prescription,
    get_doctor_prescriptions,
    get_today_appointments_for_nurse,
    ai_diagnosis,
    intake_chat,
)

st.set_page_config(page_title="CareConnect AI", layout="wide")
st.title("CareConnect AI – Talk It. Track It. Treat It.")

role = st.sidebar.selectbox("Select Role", ["Patient", "Doctor", "Nurse", "Admin"])


# =====================================================
# 1) PATIENT PORTAL (Register, Book, View, AI, Chat, Report)
# =====================================================
if role == "Patient":
    st.header("Patient Portal")

    menu = st.radio(
        "Choose Action",
        [
            "Register",
            "Book Appointment",
            "View Appointments",
            "AI Symptom Checker",
            "Chat-based Intake",
            "Paste Medical Report (AI Summary)",
        ],
    )

    # ---------- Register ----------
    if menu == "Register":
        st.subheader("Register as Patient")

        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")

        age = st.number_input("Age", 1, 120)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        blood_group = st.text_input("Blood Group")
        allergies = st.text_input("Allergies")
        medical_history = st.text_area("Medical History")

        if st.button("Register"):
            if not name or not email:
                st.error("Name and Email are required.")
            else:
                user_payload = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "role": "Patient",
                }
                user_res = create_user(user_payload)

                if user_res.status_code == 200:
                    user_id = user_res.json()["user_id"]

                    patient_payload = {
                        "user_id": user_id,
                        "age": age,
                        "gender": gender,
                        "blood_group": blood_group,
                        "allergies": allergies,
                        "medical_history": medical_history,
                    }
                    patient_res = create_patient(patient_payload)

                    if patient_res.status_code == 200:
                        st.success(f"Patient registered successfully! Patient ID: {patient_res.json()['patient_id']}")
                    else:
                        st.error(f"Failed to create patient profile: {patient_res.text}")
                else:
                    st.error(f"User registration failed: {user_res.text}")

    # ---------- Book Appointment ----------
    elif menu == "Book Appointment":
        st.subheader("Book Appointment")

        patient_id = st.text_input("Patient ID")
        doctor_id = st.text_input("Doctor ID")
        department = st.text_input("Department")
        date_val = st.date_input("Select Date", value=date.today())
        time_val = st.time_input("Select Time", value=datetime.now().time())

        schedule = datetime.combine(date_val, time_val)

        if st.button("Book"):
            payload = {
                "patient_id": patient_id,
                "doctor_id": doctor_id,
                "department": department,
                "scheduled_time": schedule.isoformat(),
            }
            res = create_appointment(payload)

            if res.status_code == 200:
                st.success("Appointment booked!")
            else:
                st.error(f"Failed to book appointment: {res.text}")

    # ---------- View Appointments ----------
    elif menu == "View Appointments":
        st.subheader("Your Appointments")

        patient_id = st.text_input("Enter Patient ID")

        if st.button("Fetch"):
            res = get_patient_appointments(patient_id)
            if res.status_code == 200:
                data = res.json()
                if data:
                    st.table(data)
                else:
                    st.info("No appointments found.")
            else:
                st.error(f"Error fetching appointments: {res.text}")

    # ---------- AI Symptom Checker ----------
    elif menu == "AI Symptom Checker":
        st.subheader("AI Symptom Checker")

        symptoms = st.text_area("Describe your symptoms")
        vitals_note = st.text_input("Additional notes (e.g., 'Fever 101°F, HR 110')", "")

        if st.button("Get AI Suggestion"):
            if not symptoms.strip():
                st.error("Please enter symptoms.")
            else:
                payload = {"symptoms": symptoms, "vitals_note": vitals_note}
                res = ai_diagnosis(payload)
                if res.status_code == 200:
                    out = res.json()
                    st.write("### Possible Conditions")
                    for cond in out["possible_conditions"]:
                        st.write(f"- {cond}")
                    st.info(out["advice"])
                else:
                    st.error(f"AI service error: {res.text}")

    # ---------- Chat-based Intake ----------
    elif menu == "Chat-based Intake":
        st.subheader("Chat with CareConnect Intake Bot")

        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        for msg, sender in st.session_state["chat_history"]:
            if sender == "user":
                st.markdown(f"**You:** {msg}")
            else:
                st.markdown(f"**Bot:** {msg}")

        user_msg = st.text_input("Type your message")

        if st.button("Send"):
            if user_msg.strip():
                st.session_state["chat_history"].append((user_msg, "user"))
                res = intake_chat(user_msg)
                if res.status_code == 200:
                    bot_reply = res.json()["reply"]
                    st.session_state["chat_history"].append((bot_reply, "bot"))
                else:
                    st.error(f"Chat service error: {res.text}")
                st.experimental_rerun()

    # ---------- Paste Medical Report ----------
    elif menu == "Paste Medical Report (AI Summary)":
        st.subheader("Paste Medical Report Text")

        report_text = st.text_area("Paste discharge summary / lab report / radiology impression here")

        if st.button("Summarize Report with AI"):
            if not report_text.strip():
                st.error("Please paste some text.")
            else:
                # Reuse AI diagnosis endpoint as a simple summarizer
                payload = {"symptoms": report_text[:2000], "vitals_note": "report_text"}
                res = ai_diagnosis(payload)
                if res.status_code == 200:
                    out = res.json()
                    st.write("### Key Points / Possible Focus Areas")
                    for cond in out["possible_conditions"]:
                        st.write(f"- {cond}")
                    st.info("This is a rough heuristic summary, not real medical advice.")
                else:
                    st.error(f"AI service error: {res.text}")


# =====================================================
# 2) DOCTOR DASHBOARD
# =====================================================
elif role == "Doctor":
    st.header("Doctor Dashboard")

    doctor_id = st.text_input("Your Doctor ID")

    if not doctor_id:
        st.info("Enter your Doctor ID to load your data.")
    else:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "My Appointments",
                "My Patients",
                "Record Diagnosis",
                "Prescriptions",
                "Vitals Monitor",
            ]
        )

        # ---------- My Appointments ----------
        with tab1:
            st.subheader("My Upcoming Appointments")
            res = get_doctor_appointments(doctor_id)
            if res.status_code == 200:
                data = res.json()
                if data:
                    st.table(data)
                else:
                    st.info("No appointments found.")
            else:
                st.error(f"Error: {res.text}")

        # ---------- My Patients ----------
        with tab2:
            st.subheader("My Patients")
            res = get_doctor_patients(doctor_id)
            if res.status_code == 200:
                data = res.json()
                if data:
                    st.table(data)
                else:
                    st.info("No patients linked yet.")
            else:
                st.error(f"Error: {res.text}")

        # ---------- Record Diagnosis ----------
        with tab3:
            st.subheader("Record Diagnosis")

            col1, col2 = st.columns(2)
            with col1:
                patient_id = st.text_input("Patient ID")
                appointment_id = st.text_input("Appointment ID (optional)")
                summary = st.text_input("Short Diagnosis Summary")
            with col2:
                details = st.text_area("Detailed Notes")

            if st.button("Save Diagnosis"):
                if not (patient_id and summary):
                    st.error("Patient ID and Summary are required.")
                else:
                    payload = {
                        "patient_id": patient_id,
                        "doctor_id": doctor_id,
                        "appointment_id": appointment_id or None,
                        "summary": summary,
                        "details": details,
                    }
                    res = create_diagnosis(payload)
                    if res.status_code == 200:
                        st.success("Diagnosis saved.")
                    else:
                        st.error(f"Error saving diagnosis: {res.text}")

            st.markdown("---")
            st.subheader("My Recent Diagnoses")
            res2 = get_doctor_diagnoses(doctor_id)
            if res2.status_code == 200:
                data2 = res2.json()
                if data2:
                    st.table(data2)
                else:
                    st.info("No diagnoses recorded yet.")
            else:
                st.error(f"Error: {res2.text}")

        # ---------- Prescriptions ----------
        with tab4:
            st.subheader("Create Prescription")

            patient_id_p = st.text_input("Patient ID (for prescription)")
            medication_name = st.text_input("Medication Name")
            dosage = st.text_input("Dosage (e.g., 500 mg BID)")
            instructions = st.text_area("Instructions")
            colp1, colp2 = st.columns(2)
            with colp1:
                start_date = st.date_input("Start Date", value=date.today())
            with colp2:
                end_date = st.date_input("End Date", value=date.today())

            if st.button("Save Prescription"):
                if not (patient_id_p and medication_name):
                    st.error("Patient ID and Medication Name are required.")
                else:
                    payload = {
                        "patient_id": patient_id_p,
                        "doctor_id": doctor_id,
                        "medication_name": medication_name,
                        "dosage": dosage,
                        "instructions": instructions,
                        "start_date": start_date.isoformat(),
                        "end_date": end_date.isoformat(),
                    }
                    res = create_prescription(payload)
                    if res.status_code == 200:
                        st.success("Prescription saved.")
                    else:
                        st.error(f"Error saving prescription: {res.text}")

            st.markdown("---")
            st.subheader("My Recent Prescriptions")
            res3 = get_doctor_prescriptions(doctor_id)
            if res3.status_code == 200:
                data3 = res3.json()
                if data3:
                    st.table(data3)
                else:
                    st.info("No prescriptions recorded yet.")
            else:
                st.error(f"Error: {res3.text}")

        # ---------- Vitals Monitor ----------
        with tab5:
            st.subheader("Live Vitals Monitor")

            patient_id_v = st.text_input("Patient ID for vitals monitor")

            if st.button("Load Vitals"):
                res = get_vitals(patient_id_v)
                if res.status_code == 200:
                    data = res.json()
                    if not data:
                        st.info("No vitals found for this patient.")
                    else:
                        st.write("Latest vitals records:")
                        st.table(data)

                        # Expect keys like: heart_rate, systolic_bp, diastolic_bp, spo2, recorded_at
                        try:
                            import pandas as pd

                            df = pd.DataFrame(data)
                            if "recorded_at" in df.columns:
                                df["recorded_at"] = pd.to_datetime(df["recorded_at"])
                                df = df.sort_values("recorded_at")

                            numeric_cols = [
                                c
                                for c in df.columns
                                if c not in ["patient_id", "id", "recorded_at"] and df[c].dtype != "O"
                            ]
                            if numeric_cols:
                                st.line_chart(df.set_index("recorded_at")[numeric_cols])
                            else:
                                st.info("No numeric vitals columns to plot.")
                        except Exception as e:
                            st.warning(f"Could not plot vitals: {e}")


# =====================================================
# 3) NURSE DASHBOARD
# =====================================================
elif role == "Nurse":
    st.header("Nurse Dashboard")

    tab1, tab2 = st.tabs(["Record Vitals", "Today's Appointments"])

    # ---------- Record Vitals ----------
    with tab1:
        st.subheader("Record Patient Vitals")

        patient_id = st.text_input("Patient ID")
        heart_rate = st.number_input("Heart Rate (bpm)", 0, 300, 80)
        systolic = st.number_input("Systolic BP", 0, 300, 120)
        diastolic = st.number_input("Diastolic BP", 0, 200, 80)
        spo2 = st.number_input("SpO2 (%)", 0, 100, 98)
        temperature = st.number_input("Temperature (°C)", 30.0, 45.0, 36.5, step=0.1)

        if st.button("Save Vitals"):
            if not patient_id:
                st.error("Patient ID is required.")
            else:
                payload = {
                    "patient_id": patient_id,
                    "heart_rate": heart_rate,
                    "systolic_bp": systolic,
                    "diastolic_bp": diastolic,
                    "spo2": spo2,
                    "temperature": temperature,
                }
                res = add_vitals(payload)
                if res.status_code == 200:
                    st.success("Vitals saved.")
                else:
                    st.error(f"Error saving vitals: {res.text}")

    # ---------- Today's Appointments ----------
    with tab2:
        st.subheader("Today's Appointments")
        res = get_today_appointments_for_nurse()
        if res.status_code == 200:
            data = res.json()
            if data:
                st.table(data)
            else:
                st.info("No appointments for today.")
        else:
            st.error(f"Error fetching appointments: {res.text}")


# =====================================================
# 4) ADMIN DASHBOARD (Analytics)
# =====================================================
elif role == "Admin":
    st.header("Admin Dashboard")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Overview Stats", "All Users", "All Appointments", "All Vitals"]
    )

    # ---------- Overview Stats ----------
    with tab1:
        st.subheader("System Overview")

        res = get_admin_stats()
        if res.status_code == 200:
            stats = res.json()
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Users", stats.get("total_users", 0))
            c2.metric("Total Patients", stats.get("total_patients", 0))
            c3.metric("Total Appointments", stats.get("total_appointments", 0))
            c4.metric("Upcoming Appointments", stats.get("upcoming_appointments", 0))

            st.markdown("### Users by Role")
            roles = stats.get("roles", {})
            if roles:
                for role_name, count in roles.items():
                    st.write(f"- **{role_name}**: {count}")
            else:
                st.info("No role breakdown available.")
        else:
            st.error(f"Error fetching stats: {res.text}")

    # ---------- All Users ----------
    with tab2:
        st.subheader("All Users")
        res = get_all_users()
        if res.status_code == 200:
            data = res.json()
            if data:
                st.table(data)
            else:
                st.info("No users found.")
        else:
            st.error(f"Error: {res.text}")

    # ---------- All Appointments ----------
    with tab3:
        st.subheader("All Appointments")
        res = get_all_appointments()
        if res.status_code == 200:
            data = res.json()
            if data:
                st.table(data)
            else:
                st.info("No appointments found.")
        else:
            st.error(f"Error: {res.text}")

    # ---------- All Vitals ----------
    with tab4:
        st.subheader("All Vitals")
        res = get_all_vitals()
        if res.status_code == 200:
            data = res.json()
            if data:
                st.table(data)
            else:
                st.info("No vitals found.")
        else:
            st.error(f"Error: {res.text}")
