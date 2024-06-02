import streamlit as st
from database import *
import plotly.express as px

st.markdown("<h1 style='text-align: center;'>Welcome to the account <span style='color: #7F00FF;'>Champ</span></h1>",
                        unsafe_allow_html=True)
tabAccountInfo, tabProgressDashboard ,tabTopUsers = st.tabs(['Account Info', 'Progress Dashboards' ,'Top Users'])

with tabAccountInfo:
    last_workout_date = get_last_workout_date(email=st.session_state.global_email)

    st.markdown(f"""
        <style>
            .blur-text {{
                text-align: center;
                font-size: 1.5em;
                color: #333; /* Darker text for better contrast */
                background: rgba(255, 255, 255, 0.8); /* Slightly more opaque background */
                backdrop-filter: blur(4px);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for better separation */
                margin-top: 20px; /* Space from the top */
            }}
        </style>
        <div class='blur-text'>
            <p><strong>Email:</strong> {st.session_state.global_email}</p>
            <p><strong>Last Workout Date:</strong> {last_workout_date}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)


    col1, col2 = st.columns([0.75, 1])
    with col2:
        leave_button = st.button('Leave')
        if leave_button:
            st.session_state.global_email = None
            st.session_state.logged_or_registered = False
            st.experimental_rerun()

with tabProgressDashboard:
    info = get_patient_exercises_info(email=st.session_state.global_email)
    columns = ['email', 'exercise_type','reps', 'sets', 'success', 'weight', 'username', 'mistakes', 'date']
    df = pd.DataFrame(info,columns=columns)
    df['date'] = pd.to_datetime(df['date'])

    df = df.sort_values(by='date')

    time_period_progress = st.selectbox(
        "Select time period", ["All Time", "Last Year", "Last Month", "Last Week"],
        index=None,
        placeholder='Please select a time period to view the graphs.'
    )

    ex_type_select = st.selectbox(
        "Select exercies type(optional)", ["Deadlift", "Biceps Curl", "Squat"],
        index=None,
        placeholder='Please select a exercise type to see your progress graph.'
    )

    if time_period_progress is not None:
        if time_period_progress == "Last Year":
            start_date = pd.Timestamp.today() - pd.DateOffset(years=1)
        elif time_period_progress == "Last Month":
            start_date = pd.Timestamp.today() - pd.DateOffset(months=1)
        elif time_period_progress == "Last Week":
            start_date = pd.Timestamp.today() - pd.DateOffset(weeks=1)
        else:
            start_date = df['date'].min()
        
        filtered_df = df[df['date'] >= start_date]

        mistakes_fig = px.line(filtered_df, x='date', y='mistakes', title='Mistakes by Date', labels={'date': 'Date', 'mistakes': 'Number of Mistakes'})
        st.write(mistakes_fig)

        success_fig = px.line(filtered_df, x='date', y='success', title='Success by Date', labels={'date': 'Date', 'success': 'Success Rate'})
        st.write(success_fig)

    if ex_type_select is not None:
        weights_filtered_df = filtered_df[(filtered_df['exercise_type'] == ex_type_select) & (filtered_df['email'] == st.session_state.global_email)]
        weights_fig = px.line(weights_filtered_df, x='date', y='weight', title=f'Weights by Date for {ex_type_select}', labels={'date': 'Date', 'weight': 'Weight (kg)'})
        st.write(weights_fig)
    
with tabTopUsers:
    top_exercise_type = st.selectbox(
        "**Exercise Type**",
        ("Deadlift", "Biceps Curl", "Squat"),
        index=None,
        placeholder='Choose the exercise to view its top performers')
    
    time_period_max_weight = st.selectbox(
        "Select time period", ["All Time", "Last Year", "Last Month", "Last Week"],
        index=None,
        placeholder='Please select a time period to view the table.'
    )

    if top_exercise_type is not None and time_period_max_weight is not None:
        df = get_best_users(top_exercise_type, time_period_max_weight)
        st.write(df)