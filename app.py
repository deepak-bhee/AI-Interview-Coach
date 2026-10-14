
import streamlit as st
from pypdf import PdfReader
from dotenv import load_dotenv
from coach import analyze_profile, generate_questions, evaluate_answers,final_report

#Load the api key
load_dotenv()

#next application title
st.title("AI-INTERVIEW-COACH")

#to define pdf - reading function
#to extract from all the pages
def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


#to allow user to upload a resume in pdf format
resume_file = st.file_uploader("Upload your resume(PDF)!!", type="pdf")

#To allow users to paste the job descriptions
job_description = st.text_area("Paste the job description here!!", height=250)


#Initialize session state
if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "questions" not in st.session_state:
    st.session_state.questions = []

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "current_q" not in st.session_state:
    st.session_state.current_q = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

if "answers" not in st.session_state:
    st.session_state.answers = []


#To process the resume
if resume_file:
    resume_text = read_pdf(resume_file)

    if resume_text.strip() == "":
        st.error("PDF is empty or could not be read. Please upload a valid PDF file.")
    else:
        st.success("Uploaded!!")

        with st.expander("See extracted text"):
            st.text(resume_text)

        if st.button("Analyze my profile"):
            if job_description.strip() == "":
                st.warning("Please paste a job description first.")
            else:
                with st.spinner("Analyzing your profile..."):
                    st.session_state.pop("questions", None)
                    st.session_state.pop("evaluations", None)

                    st.session_state.resume_text = resume_text
                    st.session_state.job_description = job_description

                    st.session_state.analysis = analyze_profile(
                        resume_text,
                        job_description
                    )

                    st.session_state.questions = []
                    st.session_state.interview_started = False
                    st.session_state.current_q = 0
                    st.session_state.messages = []
                    st.session_state.answers = []


#Display profile analysis
if st.session_state.analysis is not None:
    a = st.session_state.analysis

    st.header(f"Profile analysis: {a.get('role', 'Role')}")
    st.metric("Match score", f"{a.get('Match score', 0)}%")
    st.write(a.get("summary", ""))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Matching skills")
        for skill in a.get("matching_skills", []):
            st.write("-", skill)

    with col2:
        st.subheader("Missing skills")
        for skill in a.get("missing_skills", []):
            st.write("-", skill)

    with st.expander("See raw JSON from the AI"):
        st.json(a)


#Generate interview questions
if st.session_state.analysis is not None:
    st.divider()
    st.header("Interview questions")

    #select the number of questions
    num = st.slider("How many questions?", 3, 10, 5)

    if st.button("Generate questions"):
        st.session_state.interview_started = False

        with st.spinner("Writing questions for you..."):
            result = generate_questions(
                st.session_state.analysis,
                st.session_state.resume_text,
                st.session_state.job_description,
                num,
            )

            #To store the questions
            st.session_state.questions = result.get("questions", [])
            st.session_state.current_q = 0
            st.session_state.messages = []
            st.session_state.answers = []

            st.session_state.pop("evaluations", None)

            if not st.session_state.questions:
                st.error("No questions generated. Please try again.")
            else:
                st.success("Questions generated successfully!!")


# #Display the generated questions
# if st.session_state.questions:
#     for i, q in enumerate(st.session_state.questions, start=1):
#         st.markdown(f"**Q{i}.** {q.get('question')}")
#         st.caption(f"Type: {q.get('type')} | Skill: {q.get('skill')}")


#Start the interview
if st.session_state.questions and not st.session_state.interview_started:
    if st.button("Start interview"):
        st.session_state.pop("evaluations", None)

        first_q = st.session_state.questions[0]["question"]

        st.session_state.interview_started = True
        st.session_state.current_q = 0

        st.session_state.messages = [{
            "role": "assistant",
            "content": f"**Q1.** {first_q}"
        }]

        st.session_state.answers = []
        st.rerun()


#Interview flow
if st.session_state.questions and st.session_state.interview_started:
    st.divider()
    st.header("Interview")

    questions = st.session_state.questions
    current = st.session_state.current_q
    total = len(questions)

    if total > 0:
        st.progress(
            current / total,
            text=f"Answered {current} of {total}"
        )

    #To display the conversation
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    #To collect answers from the candidate
    if current < total:
        answer = st.chat_input("Type your answer...")

        if answer and answer.strip():
            q = questions[current]

            st.session_state.messages.append({
                "role": "user",
                "content": answer
            })

            st.session_state.answers.append({
                "question": q.get("question"),
                "type": q.get("type"),
                "skill": q.get("skill"),
                "answer": answer
            })

            st.session_state.current_q += 1
            nxt = st.session_state.current_q

            if nxt < total:
                next_text = (
                    f"**Q{nxt + 1}.** "
                    f"{questions[nxt]['question']}"
                )
            else:
                next_text = "That's the end of the interview. Thank you!"

            st.session_state.messages.append({
                "role": "assistant",
                "content": next_text
            })

            st.rerun()

    else:
        st.success("Interview complete! Your answers are saved.")


#Evaluate interview answers
if (
    st.session_state.get("interview_started")
    and st.session_state.get("answers")
    and st.session_state.current_q >= len(st.session_state.questions)
):
    if st.button("Evaluate my answers"):
        with st.spinner("Evaluating your answers..."):
            result = evaluate_answers(
                st.session_state.answers,
                st.session_state.analysis.get("role", "this role")
            )

            st.session_state.evaluations = result.get("evaluations", [])


#Display interview feedback
if "evaluations" in st.session_state:
    st.divider()
    st.header("Interview feedback")

    for i, item in enumerate(st.session_state.evaluations, start=1):
        st.subheader(f"Question {i}")
        st.write(f"Relevance: {item.get('relevance', 0)}/10")
        st.write(f"Depth: {item.get('depth', 0)}/10")
        st.write(f"Clarity: {item.get('clarity', 0)}/10")
        st.write(f"Examples: {item.get('examples', 0)}/10")
        st.write(item.get("feedback", ""))
        st.info(item.get("better_answer_tip", ""))


# Display the final scorecard and improvement plan
if st.session_state.get("interview_started") and "evaluations" in st.session_state:
    st.divider()
    st.header("Final scorecard")

    evals = st.session_state.evaluations

    # Calculate the overall score from the four evaluation criteria
    overall = round(
        sum(
            sum(e.get(area, 0) for area in [
                "relevance", "depth", "clarity", "examples"
            ])
            for e in evals
        ) / (len(evals) * 4),
        1
    )

    if overall >= 7.5:
        readiness = "Ready for interviews"
    elif overall >= 5:
        readiness = "Almost ready; more practice recommended"
    else:
        readiness = "More practice needed"

    col1, col2 = st.columns(2)

    col1.metric("Interview score", f"{overall}/10")

    col2.metric(
        "Resume match",
        f"{st.session_state.analysis.get('match_score', 0)}%"
    )

    st.subheader(readiness)

    st.markdown("#### Score by rubric area")

    for area in ["relevance", "depth", "clarity", "examples"]:
        avg = sum(e.get(area, 0) for e in evals) / len(evals)

        st.write(f"{area.title()}: {avg:.1f}/10")
        st.progress(min(avg / 10, 1.0))

    # Generate the improvement plan
    if st.button("Get my improvement plan"):
        with st.spinner("Preparing your personal feedback..."):
            st.session_state.report = final_report(
                st.session_state.analysis,
                st.session_state.answers,
                evals
            )

    if "report" in st.session_state:
        report = st.session_state.report

        st.markdown("#### Strengths")

        for item in report.get("strengths", []):
            st.write("-", item)

        st.markdown("#### Areas to improve")

        for item in report.get("improvements", []):
            st.write("-", item)

        st.markdown("#### Study plan")

        for item in report.get("study_plan", []):
            st.write("-", item)

        st.success(report.get("message", ""))

        lines = [
            "AI INTERVIEW COACH - SCORECARD",
            f"Role: {st.session_state.analysis.get('role', '')}",
            f"Interview score: {overall}/10",
            f"Resume match: {st.session_state.analysis.get('match_score', 0)}%",
            f"Readiness: {readiness}",
            "",
            "STRENGTHS:",
            *[f"- {x}" for x in report.get("strengths", [])],
            "",
            "AREAS TO IMPROVE:",
            *[f"- {x}" for x in report.get("improvements", [])],
            "",
            "STUDY PLAN:",
            *[f"- {x}" for x in report.get("study_plan", [])],
        ]

        st.download_button(
            "Download scorecard",
            "\n".join(lines),
            file_name="interview_scorecard.txt"
        )
