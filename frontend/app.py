import requests
import streamlit as st

from api_client import (
    get_current_user,
    login_user,
    register_user,
)

from pages.profile import show_profile_page


BACKEND_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Placement Intelligence Platform",
    page_icon="🎓",
    layout="wide",
)


# ============================================================
# SESSION MANAGEMENT
# ============================================================

def initialize_session():
    if "access_token" not in st.session_state:
        st.session_state.access_token = None

    if "user" not in st.session_state:
        st.session_state.user = None

    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"


def logout():
    st.session_state.access_token = None
    st.session_state.user = None
    st.session_state.page = "Dashboard"

    st.rerun()


# ============================================================
# LOGIN
# ============================================================

def login_page():
    st.title(
        "🎓 Placement Intelligence & Career Readiness Platform"
    )

    st.subheader("Login")

    with st.form("login_form"):

        email = st.text_input(
            "Email",
            placeholder="Enter your email",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
        )

        submitted = st.form_submit_button(
            "Login",
            use_container_width=True,
        )

    if submitted:

        if not email or not password:
            st.warning(
                "Please enter both email and password."
            )
            return

        try:

            response = login_user(
                email=email,
                password=password,
            )

            if response.status_code == 200:

                data = response.json()

                st.session_state.access_token = data[
                    "access_token"
                ]

                user_response = get_current_user(
                    st.session_state.access_token
                )

                if user_response.status_code == 200:

                    st.session_state.user = (
                        user_response.json()
                    )

                st.success("Login successful.")

                st.rerun()

            elif response.status_code in (400, 401):

                st.error(
                    "Invalid email or password."
                )

            else:

                st.error(
                    f"Login failed: {response.text}"
                )

        except Exception as error:

            st.error(
                f"Unable to connect to backend: {error}"
            )


# ============================================================
# REGISTRATION
# ============================================================

def register_page():

    st.title(
        "🎓 Placement Intelligence Platform"
    )

    st.subheader("Create Student Account")

    with st.form("register_form"):

        full_name = st.text_input(
            "Full Name",
            placeholder="Enter your full name",
        )

        email = st.text_input(
            "Email",
            placeholder="Enter your email",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Confirm your password",
        )

        submitted = st.form_submit_button(
            "Create Account",
            use_container_width=True,
        )

    if submitted:

        if not full_name or not email or not password:

            st.warning(
                "Please fill all required fields."
            )

            return

        if password != confirm_password:

            st.error(
                "Passwords do not match."
            )

            return

        try:

            response = register_user(
                email=email,
                full_name=full_name,
                password=password,
            )

            if response.status_code in (200, 201):

                st.success(
                    "Account created successfully. "
                    "You can now login."
                )

            elif response.status_code == 409:

                st.warning(
                    "An account with this email "
                    "already exists."
                )

            elif response.status_code == 422:

                st.error(
                    "Please enter valid registration "
                    "information."
                )

            else:

                st.error(
                    f"Registration failed: {response.text}"
                )

        except Exception as error:

            st.error(
                f"Unable to connect to backend: {error}"
            )


# ============================================================
# DASHBOARD
# ============================================================

def dashboard_page():

    st.title(
        "📊 Placement Intelligence Dashboard"
    )

    user = st.session_state.get("user")

    if user:

        full_name = user.get(
            "full_name",
            "Student",
        )

        st.subheader(
            f"Welcome, {full_name} 👋"
        )

    st.write(
        """
        Welcome to your Placement Intelligence dashboard.

        The platform analyzes your resume, profile,
        skills, projects, experience and career goals
        to estimate your career readiness.
        """
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Resume Readiness",
            "Coming soon",
        )

    with col2:

        st.metric(
            "Placement Readiness",
            "Coming soon",
        )

    with col3:

        st.metric(
            "Job Match",
            "Coming soon",
        )

    st.info(
        "Use the navigation menu to manage your profile "
        "and analyze your resume."
    )


# ============================================================
# READINESS API
# ============================================================

def get_readiness_prediction(
    api_url: str,
    token: str,
    resume_id: int,
):

    try:

        response = requests.post(
            f"{api_url}/readiness/{resume_id}/predict",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
            timeout=30,
        )

    except requests.exceptions.ConnectionError:

        st.error(
            "Unable to connect to the FastAPI backend. "
            "Make sure Uvicorn is running."
        )

        return None

    except requests.exceptions.Timeout:

        st.error(
            "The readiness prediction request timed out."
        )

        return None

    except requests.exceptions.RequestException as error:

        st.error(
            f"Request failed: {error}"
        )

        return None

    if response.status_code == 200:

        return response.json()

    if response.status_code == 401:

        st.error(
            "Your session has expired. "
            "Please login again."
        )

        return None

    if response.status_code == 404:

        st.error(
            "The selected resume was not found."
        )

        return None

    if response.status_code == 422:

        try:

            detail = response.json().get(
                "detail",
                "Unable to generate prediction.",
            )

        except Exception:

            detail = response.text

        st.error(
            f"Prediction error: {detail}"
        )

        return None

    st.error(
        f"Unable to generate readiness prediction. "
        f"HTTP {response.status_code}"
    )

    return None


# ============================================================
# DISPLAY READINESS RESULT
# ============================================================

def display_readiness_result(
    result: dict,
):

    st.subheader(
        "📈 Placement Readiness Result"
    )

    score = float(
        result.get(
            "readiness_score",
            0,
        )
    )

    probability = float(
        result.get(
            "readiness_probability",
            0,
        )
    )

    prediction = int(
        result.get(
            "prediction",
            0,
        )
    )

    model_version = result.get(
        "model_version",
        "Unknown",
    )

    # --------------------------------------------------------
    # Main metrics
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Readiness Score",
            f"{score:.2f}%",
        )

    with col2:

        st.metric(
            "Model Probability",
            f"{probability * 100:.2f}%",
        )

    with col3:

        if prediction == 1:
            prediction_text = "Ready"
        else:
            prediction_text = "Needs Improvement"

        st.metric(
            "Prediction",
            prediction_text,
        )

    st.caption(
        f"Model version: {model_version}"
    )

    st.progress(
        min(max(score / 100, 0.0), 1.0)
    )

    # --------------------------------------------------------
    # Features
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🔎 Features Used by the Model"
    )

    features = result.get(
        "features",
        {},
    )

    if features:

        feature_columns = st.columns(3)

        for index, (name, value) in enumerate(
            features.items()
        ):

            with feature_columns[index % 3]:

                readable_name = (
                    name.replace(
                        "_",
                        " ",
                    ).title()
                )

                if isinstance(value, float):

                    display_value = round(
                        value,
                        2,
                    )

                else:

                    display_value = value

                st.metric(
                    readable_name,
                    display_value,
                )

    else:

        st.info(
            "No feature information was returned."
        )

    # --------------------------------------------------------
    # Explanation
    # --------------------------------------------------------

    explanation = result.get(
        "explanation",
        {},
    )

    positive_factors = explanation.get(
        "positive_factors",
        [],
    )

    improvement_areas = explanation.get(
        "improvement_areas",
        [],
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "✅ Positive Factors"
        )

        if positive_factors:

            for factor in positive_factors:

                st.success(
                    str(factor)
                )

        else:

            st.info(
                "No positive factors were generated."
            )

    with col2:

        st.subheader(
            "⚠️ Improvement Areas"
        )

        if improvement_areas:

            for area in improvement_areas:

                st.warning(
                    str(area)
                )

        else:

            st.info(
                "No improvement areas were generated."
            )

    # --------------------------------------------------------
    # Disclaimer
    # --------------------------------------------------------

    st.divider()

    st.caption(
        """
        Important: This is a machine-learning-based
        career readiness estimate. It is not a guarantee
        of placement. The result depends on the data,
        features and model used by the system.
        """
    )


# ============================================================
# READINESS PAGE
# ============================================================

def readiness_page():

    st.title(
        "🤖 Placement Readiness Analysis"
    )

    st.write(
        """
        Select one of your uploaded resumes and generate
        an ML-based career readiness estimate.
        """
    )

    token = st.session_state.get(
        "access_token"
    )

    if not token:

        st.error(
            "You are not authenticated."
        )

        return

    # --------------------------------------------------------
    # Fetch user's resumes
    # --------------------------------------------------------

    try:

        response = requests.get(
            f"{BACKEND_URL}/resumes/",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
            timeout=15,
        )

    except requests.exceptions.RequestException as error:

        st.error(
            f"Unable to load resumes: {error}"
        )

        return

    if response.status_code == 401:

        st.error(
            "Your session has expired. Please login again."
        )

        return

    if response.status_code != 200:

        st.error(
            f"Unable to load resumes. "
            f"HTTP {response.status_code}"
        )

        return

    try:

        resumes = response.json()

    except ValueError:

        st.error(
            "The backend returned an invalid response."
        )

        return

    if not resumes:

        st.info(
            "No resumes found. "
            "Please upload a resume first."
        )

        return

    # --------------------------------------------------------
    # Resume selector
    # --------------------------------------------------------

    resume_options = {}

    for resume in resumes:

        resume_id = resume.get("id")

        file_name = resume.get(
            "file_name",
            "Unknown resume",
        )

        version = resume.get(
            "version",
            "?",
        )

        label = (
            f"{file_name} "
            f"(Version {version}, ID {resume_id})"
        )

        resume_options[label] = resume_id

    selected_resume = st.selectbox(
        "Select Resume",
        options=list(
            resume_options.keys()
        ),
    )

    selected_resume_id = resume_options[
        selected_resume
    ]

    st.info(
        f"Selected Resume ID: {selected_resume_id}"
    )

    # --------------------------------------------------------
    # Prediction button
    # --------------------------------------------------------

    if st.button(
        "🚀 Analyze Placement Readiness",
        use_container_width=True,
    ):

        with st.spinner(
            "Generating readiness prediction..."
        ):

            result = get_readiness_prediction(
                api_url=BACKEND_URL,
                token=token,
                resume_id=int(
                    selected_resume_id
                ),
            )

        if result:

            st.session_state[
                "latest_readiness_result"
            ] = result

            st.success(
                "Readiness analysis completed successfully."
            )

    # --------------------------------------------------------
    # Display previous/current result
    # --------------------------------------------------------

    result = st.session_state.get(
        "latest_readiness_result"
    )

    if result:

        display_readiness_result(
            result
        )


# ============================================================
# MAIN APPLICATION
# ============================================================

def main_application():

    initialize_session()

    # --------------------------------------------------------
    # Authentication
    # --------------------------------------------------------

    if not st.session_state.access_token:

        login_tab, register_tab = st.tabs(
            [
                "Login",
                "Register",
            ]
        )

        with login_tab:

            login_page()

        with register_tab:

            register_page()

        return

    # --------------------------------------------------------
    # Verify current user
    # --------------------------------------------------------

    user = st.session_state.get(
        "user"
    )

    if user is None:

        try:

            response = get_current_user(
                st.session_state.access_token
            )

            if response.status_code == 200:

                st.session_state.user = (
                    response.json()
                )

            else:

                st.session_state.access_token = None

                st.rerun()

        except Exception as error:

            st.error(
                f"Unable to verify your session: {error}"
            )

            return

    # --------------------------------------------------------
    # Sidebar
    # --------------------------------------------------------

    with st.sidebar:

        st.title(
            "🎓 Placement AI"
        )

        user = st.session_state.get(
            "user"
        )

        if user:

            st.write(
                f"**{user.get('full_name', 'Student')}**"
            )

            st.caption(
                user.get(
                    "email",
                    "",
                )
            )

        st.divider()

        page = st.radio(
            "Navigation",
            [
                "Dashboard",
                "Profile",
                "Resume",
                "Job Analysis",
                "Readiness Analysis",
                "Career Roadmap",
                "Interview Preparation",
                "AI Assistant",
            ],
        )

        st.divider()

        if st.button(
            "Logout",
            use_container_width=True,
        ):

            logout()

    # --------------------------------------------------------
    # Page routing
    # --------------------------------------------------------

    if page == "Dashboard":

        dashboard_page()

    elif page == "Profile":

        show_profile_page()

    elif page == "Resume":

        st.title(
            "📄 Resume Management"
        )

        st.info(
            "Resume management module is available "
            "through the backend APIs."
        )

    elif page == "Job Analysis":

        st.title(
            "💼 Job Description Analysis"
        )

        st.info(
            "Job Description analysis will be added "
            "in the upcoming module."
        )

    elif page == "Readiness Analysis":

        readiness_page()

    elif page == "Career Roadmap":

        st.title(
            "🗺️ Career Roadmap"
        )

        st.info(
            "The personalized career roadmap will be "
            "implemented after skill-gap analysis."
        )

    elif page == "Interview Preparation":

        st.title(
            "🎤 Interview Preparation"
        )

        st.info(
            "AI interview question generation will be "
            "implemented after resume and Job Description "
            "analysis."
        )

    elif page == "AI Assistant":

        st.title(
            "🤖 AI Career Assistant"
        )

        st.info(
            "The Ollama + RAG assistant will be implemented "
            "in the AI module."
        )


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main_application()