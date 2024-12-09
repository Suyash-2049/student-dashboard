import pandas as pd
import streamlit as st
import plotly.express as px

# Function to display student cards with improved layout and style
def display_student_cards(df):
    num_columns = 4  # Number of columns in the grid
    card_style = """
        background-color: #000000;  /* Black card background */
        color: #ffffff;            /* White text */
        padding: 15px;
        border-radius: 10px;
        margin: 15px;
        box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.3);
        text-align: center;
        font-family: Arial, sans-serif;
    """
    for i in range(0, len(df), num_columns):
        cols = st.columns(num_columns)  # Create a row with multiple columns
        for j, col in enumerate(cols):
            if i + j < len(df):
                student = df.iloc[i + j]
                with col:
                    st.markdown(f"<div style='{card_style}'>", unsafe_allow_html=True)
                    if student["Profile Picture URL"]:
                        st.image(student["Profile Picture URL"], width=120, use_container_width=False)
                    else:
                        st.markdown("No Image Available")
                    st.markdown(f"**{student['Name']}**", unsafe_allow_html=True)
                    st.markdown(f"Roll No: {student['Roll No']}")
                    st.markdown(f"Grade: {student['Grade']} | Division: {student['Division']}")
                    st.markdown("</div>", unsafe_allow_html=True)

# Streamlit app
def main():
    # Add custom Streamlit theme
    st.markdown(
        """
        <style>
        .main {
            background-color: #f9f9f9;  /* Light background */
            font-family: Arial, sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #000000;  /* Black text */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Class Dashboard")
    st.sidebar.title("Class Details")

    # Load Excel file from the backend
    try:
        df = pd.read_excel("Student Dash-2.xlsx")
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return

    # Display class details at the top
    class_details = df[["Grade", "Division", "Class Teacher"]].iloc[0]  # Assuming all rows belong to the same class
    st.markdown(f"### Grade: {class_details['Grade']}, Division: {class_details['Division']}")
    st.markdown(f"#### Class Teacher: {class_details['Class Teacher']}")

    # Display student cards
    st.markdown("---")
    st.markdown("### Student Cards")
    display_student_cards(df)

    # Add dropdown for graphs
    st.markdown("---")
    st.markdown("### Graphs")
    graph_type = st.selectbox("Select Graph Type", ["Student Performance", "Subject Performance"])

    if graph_type == "Student Performance":
        student = st.selectbox("Select Student", df["Name"].unique())
        student_data = df[df["Name"] == student].melt(
            id_vars=["Roll No", "Name"], value_vars=["Math", "English", "Science", "History", "Marathi"],
            var_name="Subject", value_name="Marks",
        )
        fig = px.bar(
            student_data,
            x="Subject",
            y="Marks",
            title=f"Performance of {student}",
            color="Subject",
            template="plotly_white",
            text="Marks",
            color_discrete_sequence=px.colors.qualitative.Set1,  # A complementary palette
        )
        fig.update_layout(
            title_font=dict(size=22, color="#000000"),
            xaxis=dict(title="Subjects", tickfont=dict(size=12)),
            yaxis=dict(title="Marks", tickfont=dict(size=12)),
            margin=dict(l=40, r=40, t=40, b=40),
            plot_bgcolor="#ffffff",
            paper_bgcolor="#f9f9f9",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif graph_type == "Subject Performance":
        subject = st.selectbox("Select Subject", ["Math", "English", "Science", "History", "Marathi"])
        subject_data = df[["Name", subject]].rename(columns={subject: "Marks"})
        fig = px.bar(
            subject_data,
            x="Name",
            y="Marks",
            title=f"{subject} Performance",
            color="Name",
            template="plotly_white",
            text="Marks",
            color_discrete_sequence=px.colors.qualitative.Set2,  # A complementary palette
        )
        fig.update_layout(
            title_font=dict(size=22, color="#000000"),
            xaxis=dict(title="Students", tickfont=dict(size=12)),
            yaxis=dict(title="Marks", tickfont=dict(size=12)),
            margin=dict(l=40, r=40, t=40, b=40),
            plot_bgcolor="#ffffff",
            paper_bgcolor="#f9f9f9",
        )
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
