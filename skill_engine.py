import streamlit as st
import os
import json
import re
from difflib import SequenceMatcher

SKILL_ALIASES = {
    "python": ["python"],
    "java": ["java"],
    "c": [" c ", "c programming", "c language"],
    "c++": ["c++", "cpp"],
    "javascript": ["javascript", "js"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "sql": ["sql", "mysql", "postgresql", "postgres"],
    "mongodb": ["mongodb", "mongo db"],
    "git": ["git", "github", "gitlab"],
    "excel": ["excel", "microsoft excel"],
    "power bi": ["power bi", "powerbi"],
    "tableau": ["tableau"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "natural language processing": [
        "natural language processing",
        "nlp"
    ],
    "generative ai": [
        "generative ai",
        "genai",
        "gen ai"
    ],
    "llm": [
        "llm",
        "large language model",
        "large language models"
    ],
    "ollama": ["ollama"],
    "streamlit": ["streamlit"],
    "chromadb": ["chromadb", "chroma db"],
    "langchain": ["langchain"],
    "data science": ["data science"],
    "data analysis": [
        "data analysis",
        "data analytics"
    ],
    "statistics": [
        "statistics",
        "statistical analysis"
    ],
    "aws": [
        "aws",
        "amazon web services"
    ],
    "azure": [
        "azure",
        "microsoft azure"
    ],
    "docker": ["docker"],
    "kubernetes": [
        "kubernetes",
        "k8s"
    ],
    "rest api": [
        "rest api",
        "restful api",
        "rest apis"
    ],
    "flask": ["flask"],
    "django": ["django"],
    "spring boot": ["spring boot"],
}

ROADMAP = {

    "python": {
        "goal": "Strengthen programming fundamentals and write clean Python programs.",
        "topics": "Functions, collections, file handling, exceptions, modules, OOP.",
        "project": "Build a command-line student record manager."
    },

    "sql": {
        "goal": "Become comfortable querying and analyzing relational data.",
        "topics": "SELECT, JOIN, GROUP BY, subqueries, views, aggregate functions.",
        "project": "Build a student performance database and write 15 analysis queries."
    },

    "pandas": {
        "goal": "Learn practical data cleaning and analysis.",
        "topics": "DataFrames, filtering, grouping, merging, missing values, CSV files.",
        "project": "Analyze a real-world CSV dataset and create a small report."
    },

    "machine learning": {
        "goal": "Understand the complete machine-learning workflow.",
        "topics": "Preprocessing, train/test split, regression, classification, evaluation.",
        "project": "Build a simple student-placement prediction model."
    },

    "scikit-learn": {
        "goal": "Use standard machine-learning algorithms in Python.",
        "topics": "Pipelines, preprocessing, classification, clustering, model evaluation.",
        "project": "Compare three classification algorithms on one dataset."
    },

    "tensorflow": {
        "goal": "Learn the basics of neural-network development.",
        "topics": "Tensors, layers, activation functions, loss, optimizers, training.",
        "project": "Build a basic image or text classification model."
    },

    "power bi": {
        "goal": "Create professional interactive data dashboards.",
        "topics": "Data import, transformations, relationships, visuals, DAX basics.",
        "project": "Create an internship/placement analytics dashboard."
    },

    "git": {
        "goal": "Manage code and collaborate using Git.",
        "topics": "clone, add, commit, branch, merge, pull, push, GitHub.",
        "project": "Publish this project on GitHub with meaningful commits."
    },

    "generative ai": {
        "goal": "Understand how modern AI applications use large language models.",
        "topics": "Prompts, context, hallucination, structured outputs, AI application design.",
        "project": "Create an AI study assistant."
    },

    "llm": {
        "goal": "Build useful applications around large language models.",
        "topics": "Prompt design, context, model selection, response control.",
        "project": "Build a small career guidance chatbot."
    },

    "ollama": {
        "goal": "Run and integrate a local language model.",
        "topics": "Model installation, chat API, system prompts, local inference.",
        "project": "Connect a local Llama model to the Streamlit app."
    },

    "streamlit": {
        "goal": "Build a clean Python-based web application.",
        "topics": "Widgets, layouts, session state, file upload, charts.",
        "project": "Turn a Python data project into a Streamlit dashboard."
    },

    "chromadb": {
        "goal": "Understand vector storage and semantic retrieval.",
        "topics": "Collections, embeddings, documents, similarity search.",
        "project": "Build a small semantic search system for learning resources."
    },

    "natural language processing": {
        "goal": "Process and understand text using NLP techniques.",
        "topics": "Tokenization, normalization, keyword extraction, similarity.",
        "project": "Build a job-description skill extractor."
    },

    "data science": {
        "goal": "Understand the end-to-end data science workflow.",
        "topics": "EDA, preprocessing, visualization, statistics, modeling.",
        "project": "Perform EDA on a public dataset and present findings."
    },

    "data analysis": {
        "goal": "Turn raw data into useful insights.",
        "topics": "Cleaning, aggregation, visualization, interpretation.",
        "project": "Analyze internship or placement data."
    },

    "javascript": {
        "goal": "Build interactive web functionality.",
        "topics": "Variables, functions, DOM, events, arrays, async basics.",
        "project": "Create a small interactive portfolio page."
    },

    "html": {
        "goal": "Create structured web pages.",
        "topics": "Semantic HTML, forms, tables, accessibility.",
        "project": "Build a resume portfolio page."
    },

    "css": {
        "goal": "Create responsive and attractive web interfaces.",
        "topics": "Selectors, box model, flexbox, grid, responsive design.",
        "project": "Style a responsive student portfolio."
    },

    "rest api": {
        "goal": "Understand how applications communicate through APIs.",
        "topics": "HTTP methods, JSON, endpoints, status codes, authentication basics.",
        "project": "Build a small Python API and consume it from a client."
    },

    "flask": {
        "goal": "Build lightweight Python web APIs.",
        "topics": "Routes, requests, JSON responses, templates.",
        "project": "Create a student skill API."
    },

    "docker": {
        "goal": "Package applications consistently.",
        "topics": "Images, containers, Dockerfile, ports, volumes.",
        "project": "Containerize the Streamlit application."
    },
}

def normalize(text):
    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9+#.\- ]+",
        " ",
        text
    )

    return re.sub(
        r"\s+",
        " ",
        text
    ).strip()


def extract_skills(text):
    normalized = " " + normalize(text) + " "

    found = []

    for canonical, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            a = normalize(alias)

            if f" {a} " in normalized or a in normalized:
                found.append(canonical)
                break

    return sorted(set(found))


def similarity(a, b):
    return SequenceMatcher(
        None,
        normalize(a),
        normalize(b)
    ).ratio()


def compare_skills(current_skills, required_skills):

    current = set(current_skills)

    matched = []
    partial = []
    missing = []

    for req in required_skills:

        if req in current:
            matched.append(req)
            continue

        best = max(
            (
                similarity(req, c)
                for c in current
            ),
            default=0
        )

        if best >= 0.72:
            partial.append(req)
        else:
            missing.append(req)

    return matched, partial, missing


def calculate_match_score(
    matched,
    partial,
    required
):

    total = len(required)

    if total == 0:
        return 0

    score = (
        len(matched)
        + 0.5 * len(partial)
    ) / total * 100

    return round(score)


def build_roadmap(missing):

    roadmap = []

    for skill in missing:

        item = ROADMAP.get(
            skill,
            {
                "goal": f"Build practical knowledge of {skill}.",

                "topics": (
                    f"Learn the fundamentals of {skill}, "
                    "practice common tasks, and review real examples."
                ),

                "project": (
                    f"Build a small project demonstrating {skill}."
                )
            }
        )

        roadmap.append(
            {
                "skill": skill.title(),
                **item
            }
        )

    return roadmap


st.set_page_config(
    page_title="Internship Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Internship Skill Gap Analyzer")

st.write(
    "Enter your current skills and paste a job description "
    "to identify missing skills and generate a learning roadmap."
)

st.header("1. Enter Your Current Skills")

current_input = st.text_area(
    "Your Skills",
    placeholder="Example: Python, SQL, HTML, CSS, Git",
    height=120
)


st.header("2. Enter Job Description")

job_description = st.text_area(
    "Job Description",
    placeholder=(
        "Paste the internship or job description here..."
    ),
    height=250
)


if st.button(
    "🔍 Analyze Skill Gap",
    type="primary"
):

    if not current_input.strip():

        st.warning(
            "Please enter your current skills."
        )

    elif not job_description.strip():

        st.warning(
            "Please enter a job description."
        )

    else:

        current_skills = extract_skills(
            current_input
        )

        required_skills = extract_skills(
            job_description
        )

        matched, partial, missing = compare_skills(
            current_skills,
            required_skills
        )

        score = calculate_match_score(
            matched,
            partial,
            required_skills
        )

        roadmap = build_roadmap(
            missing
        )

        result = {
            "current_skills": current_skills,
            "required_skills": required_skills,
            "matched_skills": matched,
            "partial_skills": partial,
            "missing_skills": missing,
            "match_score": score,
            "roadmap": roadmap
        }

        st.header("📊 Analysis Result")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Match Score",
                f"{score}%"
            )

        with col2:
            st.metric(
                "Matched Skills",
                len(matched)
            )

        with col3:
            st.metric(
                "Missing Skills",
                len(missing)
            )


        st.subheader("✅ Your Skills")

        if current_skills:
            st.write(
                ", ".join(
                    skill.title()
                    for skill in current_skills
                )
            )
        else:
            st.write("No recognized skills found.")


        st.subheader("📌 Required Skills")

        if required_skills:
            st.write(
                ", ".join(
                    skill.title()
                    for skill in required_skills
                )
            )
        else:
            st.write("No recognized skills found.")


        st.subheader("🟢 Matched Skills")

        if matched:

            for skill in matched:
                st.success(
                    skill.title()
                )

        else:
            st.info(
                "No matched skills found."
            )


        st.subheader("🟡 Partially Matched Skills")

        if partial:

            for skill in partial:
                st.warning(
                    skill.title()
                )

        else:
            st.info(
                "No partially matched skills."
            )


        st.subheader("🔴 Missing Skills")

        if missing:

            for skill in missing:
                st.error(
                    skill.title()
                )

        else:

            st.success(
                "🎉 No major skill gaps found!"
            )

        st.header("📚 Learning Roadmap")

        if roadmap:

            for item in roadmap:

                with st.expander(
                    f"📖 {item['skill']}"
                ):

                    st.write(
                        "**Goal:**",
                        item["goal"]
                    )

                    st.write(
                        "**Topics:**",
                        item["topics"]
                    )

                    st.write(
                        "**Mini Project:**",
                        item["project"]
                    )

        else:

            st.success(
                "You already have all the required skills!"
            )


        st.header("📥 Download Result")

        json_data = json.dumps(
            result,
            indent=2
        )

        st.download_button(
            label="Download Analysis as JSON",
            data=json_data,
            file_name="skill_gap_result.json",
            mime="application/json"
        )