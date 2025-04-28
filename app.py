import streamlit as st
from teacher_query_module import generate_teaching_prompt

theme = {
    "primaryColor": "#F39C12",
    "backgroundColor": "#FFFFFF",
    "secondaryBackgroundColor": "#F0F2F6",
    "textColor": "#000000",
    "font": "sans serif"
}

st.set_page_config(page_title="Teach with PodFlip", layout="centered")

col1, col2, col3 = st.columns([1, 1, 0.5])

with col2:
    st.image("static/logo.png", width=100)

st.title("PodFlip")
st.markdown("Flip Your Classroom with Cabrera Lab Podcasts")

if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""
if "results" not in st.session_state:
    st.session_state.results = []

prompt = st.text_area(
    "Provide a little information about your course: <b>[Name, Grade level, and topic of interest]</b>",
    height=150
)

if st.button("Suggest"):
    if prompt.strip():
        st.session_state.last_prompt = prompt.strip()
        with st.spinner("Finding the most relevant episode and generating your teaching material..."):
            result = generate_teaching_prompt(st.session_state.last_prompt)
        st.session_state.results = [result]  # clear previous
    else:
        st.warning("Please enter a topic to continue.")

if st.session_state.results:
    for idx, result in enumerate(st.session_state.results):
        with st.container():
            st.markdown("---")
            st.markdown("🎧 Watch this episode:")
            st.video(result['url'])
            st.markdown(f"{result['student_question']}")
            st.markdown(f"{result['answer_key']}")

    if st.button("🔁 Try another"):
        with st.spinner("Fetching another alternative..."):
            new_result = generate_teaching_prompt(st.session_state.last_prompt)
        st.session_state.results.append(new_result)
        st.rerun()
