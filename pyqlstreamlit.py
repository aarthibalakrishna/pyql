import streamlit as st
import pandas as pd
import mysql.connector
# Create a connection function
st.set_page_config(
    page_title="PYQL App",
    layout="wide",   # "centered" (default) or "wide"
    initial_sidebar_state="expanded"  # optional
)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #6553a6;
        background-image: url("https://www.transparenttextures.com/patterns/skulls.png");

        background-repeat: repeat;
        background-size: auto;
    }
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp span, .stApp label {
        color: #000000 !important;   /* darker text */          /* slightly larger */
    }
    <hr style="border:2px solid #000000; border-radius: 5px;">
    </style>
    """,
    unsafe_allow_html=True
)
conn = mysql.connector.connect(
    host=st.secrets["connections"]["mysql"]["host"],
    port=st.secrets["connections"]["mysql"]["port"],
    database=st.secrets["connections"]["mysql"]["database"],
    user=st.secrets["connections"]["mysql"]["username"],
    password=st.secrets["connections"]["mysql"]["password"]
)
cursor=conn.cursor()
cursor.execute("SELECT * FROM student_record")
rows = cursor.fetchall() 
st.title(":cherry_blossom: PYQL: PYTHON AND SQL IN ONE PLACE :cherry_blossom: ")
st.divider()
st.header(":cherry_blossom: Student Record Management:cherry_blossom:")
selected_student=st.radio(
    "Select Action",
    options=["INSERT", "UPDATE", "DELETE", "SELECT","DROP"],
    index=0,
    key="student_action"
)
st.divider() 
if selected_student == "INSERT":
    st.subheader(":tulip: :red[Insert Student Record]")
    id= st.text_input("ID")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    grade = st.text_input("Grade")
    if st.button("Insert"):
        cursor.execute("INSERT INTO student_record (id,name, age, grade) VALUES (%s,%s, %s, %s)", (id,name, age, grade))
        conn.commit()
        st.toast("Record inserted successfully!",icon="✅")
elif selected_student == "UPDATE":
    st.subheader(":tulip: :red[Update Student Record]")
    id_to_update = st.text_input("ID to Update")
    name = st.text_input("New Name")   
    age = st.number_input("New Age", min_value=1, max_value=100)
    grade = st.text_input("New Grade")
    if st.button("Update"):
        cursor.execute("UPDATE student_record SET name=%s, age=%s, grade=%s WHERE id=%s", (name, age, grade, id_to_update))
        conn.commit()
        st.toast("Record updated successfully!",icon="✅")
if selected_student=="SELECT":
    st.checkbox("Show All Records", key="show_all")
    st.checkbox("Show Student Records", key="show_student")
    st.subheader(":tulip: :red[Select Student Record]")
    if st.session_state.get("show_student", False):
        id_to_select = st.text_input("ID to Select")
        if id_to_select:
            cursor.execute("SELECT * FROM student_record WHERE id=%s", (id_to_select,))
            selected_row = cursor.fetchone()
            if selected_row:
                df = pd.DataFrame([selected_row], columns=["ID", "Name", "Age", "Grade"])
                st.dataframe(df)
            else:
                st.warning("No record found with that ID.")
    if st.session_state.get("show_all", False):
        st.subheader(":tulip: :red[All Student Records]")
        if rows:
            df = pd.DataFrame(rows, columns=["ID", "Name", "Age", "Grade"])
            st.dataframe(df)
elif selected_student == "DELETE":
    st.subheader(":tulip: :red[Delete Student Record]")
    id_to_delete = st.text_input("ID to Delete")
    if st.button("Delete"):
        cursor.execute("DELETE FROM student_record WHERE id=%s", (id_to_delete,))
        conn.commit()
        st.toast("Record deleted successfully!",icon="✅")
    st.subheader(":tulip: :red[Select Student Record]")
    if rows:
        df = pd.DataFrame(rows, columns=["ID", "Name", "Age", "Grade"])
        st.dataframe(df)
elif selected_student == "DROP":
    st.subheader(":tulip: :red[Drop Student Record Table]")
    if st.button("Drop Table"):
        cursor.execute("DROP TABLE IF EXISTS student_record")
        conn.commit()
        st.toast("Table dropped successfully!",icon="✅")
        st.session_state["show_all"] = False
        st.session_state["show_student"] = False
        st.session_state["refresh_button"] = False

st.divider() 
st.button("Refresh", key="refresh_button")
if st.session_state.get("refresh_button", False):
    cursor.execute("SELECT * FROM student_record")
    rows = cursor.fetchall()
    if rows:
        df = pd.DataFrame(rows, columns=["ID", "Name", "Age", "Grade"])
        st.dataframe(df)
    else:
        st.warning("No records found.")
cursor.close()
conn.close()
