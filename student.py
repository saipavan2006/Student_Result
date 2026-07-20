import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import plotly.express as px 

st.set_page_config(page_title="Student Result Analysis")
st.title('Student Result Analysis')
st.write("Welcome to the app")

with st.sidebar:

    selected = option_menu(
        menu_title ="📌Menu",
        options = [
            "Raw Data",
            "Student Result",
            "Topper",
            "Search Student",
            "Subject Analysis",
            "Pass / Fail",
        ],
        icons = [
            "table",
            "bar-chart",
            "trophy",
            "search",
            "book",
            "check-circle",
            "grid"
        ],
        menu_icon = "menu-button-wide",
        default_index = 0
    )

df = pd.read_csv('D:\streamlit\data\student_data.csv')

if selected == 'Raw Data':
    st.subheader("📊Raw Data")
    st.dataframe(df)

elif selected == 'Student Result':
    total_marks = df.groupby('Name')['Marks'].sum()
    avg_marks = df.groupby('Name')['Marks'].mean()

    result = pd.DataFrame({"Total marks":total_marks, "Average":avg_marks}).reset_index()
    st.dataframe(result)

    fig = px.bar(result,x="Name",y="Total marks",color ="Total marks",title = "Total Marks of students")
    st.plotly_chart(fig)

    # stacked bar chart for subject-wise marks 
    st.subheader("📊Subject-wise marks of students")
    pivot_df = df.pivot_table(index="Name", columns = "Subject", values = "Marks")

    fig, ax = plt.subplots(figsize=(8,5))
    pivot_df.plot(kind = "bar", stacked=True, ax=ax)

    ax.set_title("Student Marks by Subject")
    ax.set_xlabel("Student")
    ax.set_ylabel("Marks")
    st.pyplot(fig)

elif selected == 'Topper':
    total_marks = df.groupby('Name')['Marks'].sum().sort_values(ascending=False)
    # avg_marks = df.groupby('Name')['Marks'].mean()
    n = st.number_input("How many topper do you want: ",min_value=1, max_value=len(total_marks), value=1)
    
    st.subheader(f"🏆Top {n} Students")
    st.dataframe(total_marks.head(n))

elif selected == "Search Student":
    st.subheader("🔍Search Student")
    name = st.text_input("Enter the name of the student")

    if name:
        filtered_df = df[df['Name'].str.lower() == name.lower()]
        
        if not filtered_df.empty: 
            st.success(f"Showing the result of {name}")
            st.dataframe(filtered_df)

            total_marks = filtered_df.groupby('Name')['Marks'].sum()
            avg_marks = filtered_df.groupby('Name')['Marks'].mean()

        # st.write(f"Total Marks: {total_marks}")
        # #st.write("Total marks of" name} is {total_marks}")
        # st.write(f"Average marks of {name} is {avg_marks}")

        else:
            st.error(f"{name} not found")