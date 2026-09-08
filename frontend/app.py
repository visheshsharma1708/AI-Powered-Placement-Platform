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


def login_page():
    st.title("🎓 Placement Intelligence & Career Readiness Platform")

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


def register_page():
    st.title("🎓 Placement Intelligence Platform")

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
                    "An account with this email already exists."
                )

            elif response.status_code == 422:

                st.error(
                    "Please enter valid registration information."
                )

            else:

                st.error(
                    f"Registration failed: {response.text}"
                )

        except Exception as error:

            st.error(
                f"Unable to connect to backend: {error}"
            )


def dashboard_page():
    st.title("📊 Placement Intelligence Dashboard")

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
        This platform will analyze your resume,
        skills, projects, experience and job requirements
        to estimate your career readiness.
        """
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Resume Readiness",
            "Not analyzed",
        )

    with col2:
        st.metric(
            "Placement Readiness",
            "Not calculated",
        )

    with col3:
        st.metric(
            "Skill Match",
            "Not analyzed",
        )

    st.info(
        "Complete your student profile first. "
        "Resume intelligence and job analysis will be "
        "added in the upcoming modules."
    )


def main_application():

    initialize_session()

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

    user = st.session_state.get("user")

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

        except Exception:

            st.error(
                "Unable to verify your session."
            )
            return

    with st.sidebar:

        st.title("🎓 Placement AI")

        user = st.session_state.get("user")

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

    if page == "Dashboard":

        dashboard_page()

    elif page == "Profile":

        show_profile_page()

    elif page == "Resume":

        st.title("📄 Resume Management")

        st.info(
            "Resume management will be implemented in Step 9."
        )

    elif page == "Job Analysis":

        st.title("💼 Job Description Analysis")

        st.info(
            "Job Description analysis will be implemented "
            "after the resume module."
        )

    elif page == "Readiness Analysis":

        st.title("🤖 Placement Readiness")

        st.info(
            "Machine learning readiness analysis will be "
            "implemented after the required data pipeline "
            "is ready."
        )

    elif page == "Career Roadmap":

        st.title("🗺️ Career Roadmap")

        st.info(
            "Personalized career roadmap will be implemented "
            "after skill-gap analysis."
        )

    elif page == "Interview Preparation":

        st.title("🎤 Interview Preparation")

        st.info(
            "AI interview question generation will be "
            "implemented after resume and JD analysis."
        )

    elif page == "AI Assistant":

        st.title("🤖 AI Career Assistant")

        st.info(
            "The Ollama + RAG assistant will be implemented "
            "in the AI module."
        )


if __name__ == "__main__":
    main_application()