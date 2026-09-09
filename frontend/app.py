import requests
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Placement Intelligence Platform",
    page_icon="🎓",
    layout="wide",
)


# ============================================================
# SESSION MANAGEMENT
# ============================================================

def initialize_session():
    defaults = {
        "access_token": None,
        "user": None,
        "profile": None,
        "latest_analysis": None,
        "latest_readiness": None,
        "latest_resume_id": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def logout():
    st.session_state.clear()
    st.rerun()


# ============================================================
# COMMON HELPERS
# ============================================================

def get_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }


def get_error_message(
    response,
    default_message: str,
) -> str:

    try:
        data = response.json()

        detail = data.get("detail")

        if isinstance(detail, list):

            messages = []

            for item in detail:

                if isinstance(item, dict):

                    messages.append(
                        str(
                            item.get(
                                "msg",
                                item,
                            )
                        )
                    )

                else:

                    messages.append(
                        str(item)
                    )

            if messages:
                return "; ".join(messages)

        if detail:
            return str(detail)

    except (
        ValueError,
        AttributeError,
        TypeError,
    ):
        pass

    if response is not None:

        text = getattr(
            response,
            "text",
            "",
        )

        if text:
            return text

    return default_message


def handle_unauthorized():

    st.session_state["access_token"] = None
    st.session_state["user"] = None
    st.session_state["profile"] = None
    st.session_state["latest_analysis"] = None
    st.session_state["latest_readiness"] = None
    st.session_state["latest_resume_id"] = None

    st.warning(
        "Your session has expired. Please login again."
    )

    st.rerun()


def show_connection_error(error):

    if isinstance(
        error,
        requests.ConnectionError,
    ):

        st.error(
            "Cannot connect to FastAPI backend. "
            "Please make sure Uvicorn is running on "
            "http://127.0.0.1:8000."
        )

    elif isinstance(
        error,
        requests.Timeout,
    ):

        st.error(
            "The request timed out. "
            "Please try again."
        )

    else:

        st.error(
            f"Backend request failed: {error}"
        )


# ============================================================
# AUTHENTICATION API
# ============================================================

def login_user(
    email: str,
    password: str,
):

    return requests.post(
        f"{API_URL}/auth/login",
        json={
            "email": email.strip(),
            "password": password,
        },
        timeout=30,
    )


def register_user(
    full_name: str,
    email: str,
    password: str,
):

    return requests.post(
        f"{API_URL}/auth/register",
        json={
            "full_name": full_name.strip(),
            "email": email.strip(),
            "password": password,
        },
        timeout=30,
    )


def get_current_user(token: str):

    return requests.get(
        f"{API_URL}/users/me",
        headers=get_headers(token),
        timeout=30,
    )


# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():

    st.title(
        "🎓 Placement Intelligence "
        "& Career Readiness Platform"
    )

    st.subheader(
        "Student Login"
    )

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

    if not submitted:
        return

    if not email.strip():

        st.warning(
            "Please enter your email."
        )

        return

    if not password:

        st.warning(
            "Please enter your password."
        )

        return

    try:

        response = login_user(
            email=email,
            password=password,
        )

        if response.status_code != 200:

            st.error(
                get_error_message(
                    response,
                    "Invalid email or password.",
                )
            )

            return

        data = response.json()

        token = data.get(
            "access_token"
        )

        if not token:

            st.error(
                "Login succeeded, but no access token "
                "was returned by the backend."
            )

            return

        st.session_state["access_token"] = token

        user_response = get_current_user(
            token
        )

        if user_response.status_code == 200:

            st.session_state["user"] = (
                user_response.json()
            )

        elif user_response.status_code == 401:

            handle_unauthorized()
            return

        else:

            st.session_state["access_token"] = None
            st.session_state["user"] = None

            st.error(
                get_error_message(
                    user_response,
                    "Unable to retrieve your account information.",
                )
            )

            return

        st.success(
            "Login successful."
        )

        st.rerun()

    except requests.RequestException as error:

        show_connection_error(error)


# ============================================================
# REGISTRATION PAGE
# ============================================================

def register_page():

    st.title(
        "🎓 Create Student Account"
    )

    with st.form(
        "register_form"
    ):

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

    if not submitted:
        return

    if not full_name.strip():

        st.warning(
            "Full name is required."
        )

        return

    if not email.strip():

        st.warning(
            "Email is required."
        )

        return

    if not password:

        st.warning(
            "Password is required."
        )

        return

    if len(password) < 6:

        st.warning(
            "Password must contain at least 6 characters."
        )

        return

    if password != confirm_password:

        st.error(
            "Passwords do not match."
        )

        return

    try:

        response = register_user(
            full_name=full_name,
            email=email,
            password=password,
        )

        if response.status_code in (
            200,
            201,
        ):

            st.success(
                "Account created successfully. "
                "Please login."
            )

        else:

            st.error(
                get_error_message(
                    response,
                    "Registration failed.",
                )
            )

    except requests.RequestException as error:

        show_connection_error(error)


# ============================================================
# DASHBOARD PAGE
# ============================================================

def dashboard_page():

    user = (
        st.session_state.get("user")
        or {}
    )

    full_name = user.get(
        "full_name",
        "Student",
    )

    st.title(
        "📊 Placement Intelligence Dashboard"
    )

    st.subheader(
        f"Welcome, {full_name} 👋"
    )

    st.write(
        """
        Your centralized placement intelligence dashboard.
        Analyze your resume, evaluate your placement readiness,
        and prepare for job opportunities.
        """
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Student Profile",
            "Active",
        )

    with col2:

        st.metric(
            "Resume Intelligence",
            "Active",
        )

    with col3:

        st.metric(
            "ML Readiness",
            "Active",
        )

    with col4:

        st.metric(
            "Job Analysis",
            "Active",
        )

    st.divider()

    st.subheader(
        "🚀 Platform Workflow"
    )

    st.write(
        """
        **Step 1:** Complete your student profile.

        **Step 2:** Upload your latest resume.

        **Step 3:** Analyze your resume.

        **Step 4:** Generate placement-readiness prediction.

        **Step 5:** Add job descriptions.

        **Step 6:** Use the job-matching module to identify
        skill gaps and career opportunities.
        """
    )

    readiness = st.session_state.get(
        "latest_readiness"
    )

    if readiness:

        try:

            score = float(
                readiness.get(
                    "readiness_score",
                    0,
                )
            )

            st.divider()

            st.subheader(
                "Latest Readiness Score"
            )

            st.metric(
                "Placement Readiness",
                f"{score:.2f}%",
            )

            st.progress(
                min(
                    max(
                        score / 100,
                        0.0,
                    ),
                    1.0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            pass


# ============================================================
# PROFILE API
# ============================================================

def get_profile_api(
    token: str,
):

    return requests.get(
        f"{API_URL}/profiles/me",
        headers=get_headers(token),
        timeout=30,
    )


def create_profile_api(
    token: str,
    profile_data: dict,
):

    return requests.post(
        f"{API_URL}/profiles/me",
        headers=get_headers(token),
        json=profile_data,
        timeout=30,
    )


def update_profile_api(
    token: str,
    profile_data: dict,
):

    return requests.put(
        f"{API_URL}/profiles/me",
        headers=get_headers(token),
        json=profile_data,
        timeout=30,
    )


# ============================================================
# PROFILE PAGE
# ============================================================

def profile_page(
    token: str,
):

    st.title(
        "👤 Student Profile"
    )

    profile = {}
    profile_exists = False

    # --------------------------------------------------------
    # Load Profile
    # --------------------------------------------------------

    try:

        response = get_profile_api(
            token
        )

        if response.status_code == 200:

            profile = response.json()

            if not isinstance(
                profile,
                dict,
            ):

                st.error(
                    "Invalid profile data received from backend."
                )

                return

            profile_exists = True

            st.session_state["profile"] = profile

        elif response.status_code == 404:

            profile = {}
            profile_exists = False

            st.session_state["profile"] = None

        elif response.status_code == 401:

            handle_unauthorized()
            return

        else:

            st.error(
                get_error_message(
                    response,
                    "Unable to load profile.",
                )
            )

            return

    except requests.RequestException as error:

        show_connection_error(error)
        return

    # --------------------------------------------------------
    # Profile Status
    # --------------------------------------------------------

    if profile_exists:

        st.success(
            "Your profile is currently saved."
        )

    else:

        st.info(
            "Your profile has not been created yet. "
            "Complete the form below."
        )

    # --------------------------------------------------------
    # Profile Form
    # --------------------------------------------------------

    form_title = (
        "Update Profile"
        if profile_exists
        else "Create Student Profile"
    )

    st.subheader(
        form_title
    )

    with st.form(
        "student_profile_form"
    ):

        university = st.text_input(
            "University",
            value=(
                profile.get(
                    "university"
                )
                or ""
            ),
            placeholder=(
                "Example: University of Rajasthan"
            ),
        )

        degree = st.text_input(
            "Degree",
            value=(
                profile.get(
                    "degree"
                )
                or ""
            ),
            placeholder="Example: B.Tech",
        )

        branch = st.text_input(
            "Branch / Specialization",
            value=(
                profile.get(
                    "branch"
                )
                or ""
            ),
            placeholder=(
                "Example: Computer Science and Engineering"
            ),
        )

        current_year = profile.get(
            "graduation_year"
        )

        try:

            current_year = int(
                current_year
            )

        except (
            TypeError,
            ValueError,
        ):

            current_year = 2026

        graduation_year = st.number_input(
            "Graduation Year",
            min_value=2000,
            max_value=2100,
            value=current_year,
            step=1,
        )

        target_role = st.text_input(
            "Target Job Role",
            value=(
                profile.get(
                    "target_role"
                )
                or ""
            ),
            placeholder=(
                "Example: Machine Learning Engineer"
            ),
        )

        github_url = st.text_input(
            "GitHub URL",
            value=(
                profile.get(
                    "github_url"
                )
                or ""
            ),
            placeholder=(
                "https://github.com/username"
            ),
        )

        linkedin_url = st.text_input(
            "LinkedIn URL",
            value=(
                profile.get(
                    "linkedin_url"
                )
                or ""
            ),
            placeholder=(
                "https://www.linkedin.com/in/username"
            ),
        )

        portfolio_url = st.text_input(
            "Portfolio URL",
            value=(
                profile.get(
                    "portfolio_url"
                )
                or ""
            ),
            placeholder=(
                "https://yourportfolio.com"
            ),
        )

        bio = st.text_area(
            "Professional Bio",
            value=(
                profile.get(
                    "bio"
                )
                or ""
            ),
            placeholder=(
                "Briefly describe your technical interests, "
                "experience, and career goals."
            ),
            height=150,
        )

        submitted = st.form_submit_button(
            (
                "Update Profile"
                if profile_exists
                else "Create Profile"
            ),
            use_container_width=True,
        )

    # --------------------------------------------------------
    # Save Profile
    # --------------------------------------------------------

    if not submitted:
        return

    profile_data = {
        "university": (
            university.strip()
            or None
        ),
        "degree": (
            degree.strip()
            or None
        ),
        "branch": (
            branch.strip()
            or None
        ),
        "graduation_year": int(
            graduation_year
        ),
        "target_role": (
            target_role.strip()
            or None
        ),
        "github_url": (
            github_url.strip()
            or None
        ),
        "linkedin_url": (
            linkedin_url.strip()
            or None
        ),
        "portfolio_url": (
            portfolio_url.strip()
            or None
        ),
        "bio": (
            bio.strip()
            or None
        ),
    }

    try:

        if profile_exists:

            save_response = update_profile_api(
                token,
                profile_data,
            )

        else:

            save_response = create_profile_api(
                token,
                profile_data,
            )

        if save_response.status_code in (
            200,
            201,
        ):

            st.session_state["profile"] = (
                save_response.json()
                if save_response.content
                else profile_data
            )

            if profile_exists:

                st.success(
                    "Profile updated successfully."
                )

            else:

                st.success(
                    "Profile created successfully."
                )

            st.rerun()

        elif save_response.status_code == 401:

            handle_unauthorized()
            return

        elif save_response.status_code == 409:

            st.warning(
                "A profile already exists for this account. "
                "Please refresh the page and update the existing profile."
            )

        elif save_response.status_code == 422:

            st.error(
                "Some profile information is invalid. "
                "Please check the entered values."
            )

            st.caption(
                get_error_message(
                    save_response,
                    "Validation failed.",
                )
            )

        else:

            st.error(
                get_error_message(
                    save_response,
                    "Unable to save profile.",
                )
            )

    except requests.RequestException as error:

        show_connection_error(error)


# ============================================================
# RESUME API
# ============================================================

def get_resumes(
    token: str,
):

    return requests.get(
        f"{API_URL}/resumes/",
        headers=get_headers(token),
        timeout=30,
    )


def upload_resume_file(
    token: str,
    uploaded_file,
):

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
            or "application/octet-stream",
        )
    }

    return requests.post(
        f"{API_URL}/resumes/upload",
        files=files,
        headers=get_headers(token),
        timeout=60,
    )


def analyze_resume_api(
    token: str,
    resume_id: int,
):

    return requests.post(
        f"{API_URL}/resumes/{resume_id}/analyze",
        headers=get_headers(token),
        timeout=120,
    )


def download_resume_api(
    token: str,
    resume_id: int,
):

    return requests.get(
        f"{API_URL}/resumes/{resume_id}/download",
        headers=get_headers(token),
        timeout=60,
    )


def predict_readiness_api(
    token: str,
    resume_id: int,
):

    return requests.post(
        f"{API_URL}/readiness/{resume_id}/predict",
        headers=get_headers(token),
        timeout=120,
    )


# ============================================================
# RESUME ANALYSIS DISPLAY
# ============================================================

def display_analysis_section(
    title: str,
    data,
):

    if not data:
        return

    st.subheader(title)

    if isinstance(
        data,
        list,
    ):

        for item in data:

            if isinstance(
                item,
                dict,
            ):

                st.json(item)

            else:

                st.write(
                    f"• {item}"
                )

    else:

        st.write(data)


def display_resume_analysis(
    analysis: dict,
):

    st.divider()

    st.subheader(
        "📊 Resume Analysis"
    )

    skills = analysis.get(
        "skills",
        [],
    )

    technologies = analysis.get(
        "technologies",
        [],
    )

    projects = analysis.get(
        "projects",
        [],
    )

    experience = analysis.get(
        "experience",
        [],
    )

    education = analysis.get(
        "education",
        [],
    )

    certifications = analysis.get(
        "certifications",
        [],
    )

    achievements = analysis.get(
        "achievements",
        [],
    )

    raw_text = analysis.get(
        "raw_text",
        "",
    )

    columns = st.columns(4)

    summary = [
        ("Skills", skills),
        ("Technologies", technologies),
        ("Projects", projects),
        ("Experience", experience),
    ]

    for column, (
        label,
        value,
    ) in zip(
        columns,
        summary,
    ):

        with column:

            count = (
                len(value)
                if isinstance(
                    value,
                    list,
                )
                else 0
            )

            st.metric(
                label,
                count,
            )

    display_analysis_section(
        "🛠️ Skills",
        skills,
    )

    display_analysis_section(
        "💻 Technologies",
        technologies,
    )

    display_analysis_section(
        "🎓 Education",
        education,
    )

    display_analysis_section(
        "🚀 Projects",
        projects,
    )

    display_analysis_section(
        "💼 Experience",
        experience,
    )

    display_analysis_section(
        "📜 Certifications",
        certifications,
    )

    display_analysis_section(
        "🏆 Achievements",
        achievements,
    )

    if raw_text:

        with st.expander(
            "View Extracted Resume Text"
        ):

            st.text(raw_text)


# ============================================================
# RESUME PAGE
# ============================================================

def resumes_page(
    token: str,
):

    st.title(
        "📄 Resume Management"
    )

    st.subheader(
        "Upload Resume"
    )

    uploaded_file = st.file_uploader(
        "Choose a PDF or DOCX resume",
        type=[
            "pdf",
            "docx",
        ],
        key="resume_uploader",
    )

    if uploaded_file is not None:

        st.info(
            f"Selected file: "
            f"{uploaded_file.name} "
            f"({uploaded_file.size:,} bytes)"
        )

        if st.button(
            "⬆️ Upload Resume",
            use_container_width=True,
        ):

            try:

                response = upload_resume_file(
                    token,
                    uploaded_file,
                )

                if response.status_code == 401:

                    handle_unauthorized()
                    return

                if response.status_code == 201:

                    data = response.json()

                    resume_id = data.get(
                        "id"
                    )

                    st.session_state[
                        "latest_resume_id"
                    ] = resume_id

                    st.success(
                        "Resume uploaded successfully."
                    )

                    st.rerun()

                else:

                    st.error(
                        get_error_message(
                            response,
                            "Resume upload failed.",
                        )
                    )

            except requests.RequestException as error:

                show_connection_error(error)

    st.divider()

    st.subheader(
        "Your Resumes"
    )

    try:

        response = get_resumes(
            token
        )

        if response.status_code == 401:

            handle_unauthorized()
            return

        if response.status_code != 200:

            st.error(
                get_error_message(
                    response,
                    "Unable to load resumes.",
                )
            )

            return

        resumes = response.json()

        if not resumes:

            st.info(
                "No resumes uploaded yet."
            )

            return

        for resume in resumes:

            resume_id = resume.get(
                "id"
            )

            if resume_id is None:
                continue

            with st.container():

                col1, col2, col3 = st.columns(
                    [4, 2, 2]
                )

                with col1:

                    st.markdown(
                        f"### 📄 "
                        f"{resume.get('file_name', 'Resume')}"
                    )

                    st.caption(
                        f"Resume ID: {resume_id} | "
                        f"Version: "
                        f"{resume.get('version', '-')}"
                    )

                with col2:

                    st.write(
                        f"**Type:** "
                        f"{resume.get('file_type', '-')}"
                    )

                    size = resume.get(
                        "file_size",
                        0,
                    )

                    st.write(
                        f"**Size:** "
                        f"{size:,} bytes"
                    )

                with col3:

                    if st.button(
                        "🔍 Analyze",
                        key=f"analyze_{resume_id}",
                        use_container_width=True,
                    ):

                        run_resume_analysis(
                            token,
                            int(resume_id),
                        )

                    if st.button(
                        "⬇️ Download",
                        key=f"download_{resume_id}",
                        use_container_width=True,
                    ):

                        run_resume_download(
                            token,
                            int(resume_id),
                            resume.get(
                                "file_name",
                                "resume",
                            ),
                        )

                st.divider()

        analysis = st.session_state.get(
            "latest_analysis"
        )

        if analysis:

            display_resume_analysis(
                analysis
            )

    except requests.RequestException as error:

        show_connection_error(error)


def run_resume_analysis(
    token: str,
    resume_id: int,
):

    with st.spinner(
        "Analyzing resume..."
    ):

        try:

            response = analyze_resume_api(
                token,
                resume_id,
            )

            if response.status_code == 401:

                handle_unauthorized()
                return

            if response.status_code != 200:

                st.error(
                    get_error_message(
                        response,
                        "Resume analysis failed.",
                    )
                )

                return

            analysis = response.json()

            st.session_state[
                "latest_analysis"
            ] = analysis

            st.session_state[
                "latest_resume_id"
            ] = resume_id

            st.success(
                "Resume analysis completed successfully."
            )

            st.rerun()

        except requests.RequestException as error:

            show_connection_error(error)


def run_resume_download(
    token: str,
    resume_id: int,
    file_name: str,
):

    try:

        response = download_resume_api(
            token,
            resume_id,
        )

        if response.status_code == 401:

            handle_unauthorized()
            return

        if response.status_code != 200:

            st.error(
                get_error_message(
                    response,
                    "Resume download failed.",
                )
            )

            return

        st.download_button(
            "⬇️ Download Resume",
            data=response.content,
            file_name=file_name,
            mime="application/octet-stream",
            key=f"download_result_{resume_id}",
        )

    except requests.RequestException as error:

        show_connection_error(error)


# ============================================================
# READINESS API
# ============================================================

def readiness_page(
    token: str,
):

    st.title(
        "🎯 Placement Readiness Analysis"
    )

    st.write(
        """
        Generate an ML-based placement-readiness estimate
        using your resume and available profile information.
        """
    )

    try:

        response = get_resumes(
            token
        )

        if response.status_code == 401:

            handle_unauthorized()
            return

        if response.status_code != 200:

            st.error(
                get_error_message(
                    response,
                    "Unable to load resumes.",
                )
            )

            return

        resumes = response.json()

        if not resumes:

            st.info(
                "Please upload a resume first."
            )

            return

        resume_options = {}

        for resume in resumes:

            resume_id = resume.get(
                "id"
            )

            if resume_id is None:
                continue

            file_name = resume.get(
                "file_name",
                "Resume",
            )

            version = resume.get(
                "version",
                "?",
            )

            label = (
                f"{file_name} "
                f"(Version {version}, "
                f"ID {resume_id})"
            )

            resume_options[label] = int(
                resume_id
            )

        if not resume_options:

            st.info(
                "No valid resumes were found."
            )

            return

        labels = list(
            resume_options.keys()
        )

        default_index = 0

        latest_resume_id = (
            st.session_state.get(
                "latest_resume_id"
            )
        )

        if latest_resume_id is not None:

            for index, label in enumerate(
                labels
            ):

                if (
                    resume_options[label]
                    == latest_resume_id
                ):

                    default_index = index
                    break

        selected_label = st.selectbox(
            "Select Resume",
            labels,
            index=default_index,
        )

        selected_resume_id = (
            resume_options[
                selected_label
            ]
        )

        st.info(
            f"Selected Resume ID: "
            f"{selected_resume_id}"
        )

        if st.button(
            "🚀 Generate Readiness Prediction",
            use_container_width=True,
        ):

            with st.spinner(
                "Generating ML prediction..."
            ):

                try:

                    prediction_response = (
                        predict_readiness_api(
                            token,
                            selected_resume_id,
                        )
                    )

                    if (
                        prediction_response.status_code
                        == 401
                    ):

                        handle_unauthorized()
                        return

                    if (
                        prediction_response.status_code
                        != 200
                    ):

                        st.error(
                            get_error_message(
                                prediction_response,
                                "Unable to generate readiness prediction.",
                            )
                        )

                        return

                    result = (
                        prediction_response.json()
                    )

                    st.session_state[
                        "latest_readiness"
                    ] = result

                    st.session_state[
                        "latest_resume_id"
                    ] = selected_resume_id

                    st.success(
                        "Readiness prediction generated successfully."
                    )

                except requests.RequestException as error:

                    show_connection_error(error)

        result = st.session_state.get(
            "latest_readiness"
        )

        if result:

            display_readiness_result(
                result
            )

    except requests.RequestException as error:

        show_connection_error(error)


def display_readiness_result(
    result: dict,
):

    st.divider()

    st.subheader(
        "📈 Placement Readiness Result"
    )

    try:

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

    except (
        TypeError,
        ValueError,
    ):

        st.error(
            "Invalid readiness result returned by backend."
        )

        return

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

        st.metric(
            "Prediction",
            (
                "Placement Ready"
                if prediction == 1
                else "Needs Improvement"
            ),
        )

    st.progress(
        min(
            max(
                score / 100,
                0.0,
            ),
            1.0,
        )
    )

    features = result.get(
        "features",
        {},
    )

    if (
        isinstance(
            features,
            dict,
        )
        and features
    ):

        st.divider()

        st.subheader(
            "Model Features"
        )

        columns = st.columns(3)

        for index, (
            name,
            value,
        ) in enumerate(
            features.items()
        ):

            with columns[
                index % 3
            ]:

                label = (
                    name.replace(
                        "_",
                        " ",
                    ).title()
                )

                if isinstance(
                    value,
                    float,
                ):

                    value = round(
                        value,
                        2,
                    )

                st.metric(
                    label,
                    value,
                )

    explanation = result.get(
        "explanation",
        {},
    )

    if isinstance(
        explanation,
        dict,
    ):

        positive = explanation.get(
            "positive_factors",
            [],
        )

        improvement = explanation.get(
            "improvement_areas",
            [],
        )

        if positive or improvement:

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                st.subheader(
                    "✅ Positive Factors"
                )

                if positive:

                    for item in positive:

                        display_factor(
                            item,
                            positive=True,
                        )

                else:

                    st.info(
                        "No positive factors returned."
                    )

            with col2:

                st.subheader(
                    "⚠️ Improvement Areas"
                )

                if improvement:

                    for item in improvement:

                        display_factor(
                            item,
                            positive=False,
                        )

                else:

                    st.info(
                        "No improvement areas returned."
                    )

    st.caption(
        "This score is an estimate based on available "
        "resume and profile information. It is not a "
        "guarantee of placement."
    )


def display_factor(
    item,
    positive: bool,
):

    if isinstance(
        item,
        dict,
    ):

        label = item.get(
            "label",
            item.get(
                "feature",
                "Factor",
            ),
        )

        contribution = item.get(
            "contribution"
        )

        value = item.get(
            "value"
        )

        text = f"**{label}**"

        if value is not None:

            text += (
                f" — value: {value}"
            )

        if contribution is not None:

            text += (
                f" — contribution: "
                f"{contribution}"
            )

    else:

        text = str(item)

    if positive:

        st.success(text)

    else:

        st.warning(text)


# ============================================================
# JOB DESCRIPTION PAGE
# ============================================================

def job_description_page(
    token: str,
):

    st.title(
        "💼 Job Descriptions"
    )

    st.write(
        """
        Add job descriptions that will be used for
        job matching and skill-gap analysis.
        """
    )

    with st.form(
        "job_description_form"
    ):

        title = st.text_input(
            "Job Title",
            placeholder="Machine Learning Engineer",
        )

        company_name = st.text_input(
            "Company Name",
            placeholder="Example Technologies",
        )

        description = st.text_area(
            "Job Description",
            height=250,
            placeholder=(
                "Paste the complete job description here..."
            ),
        )

        submitted = st.form_submit_button(
            "Save Job Description",
            use_container_width=True,
        )

    if submitted:

        if not title.strip():

            st.error(
                "Job title is required."
            )

            return

        if len(
            description.strip()
        ) < 20:

            st.error(
                "Job description must contain "
                "at least 20 characters."
            )

            return

        payload = {
            "title": title.strip(),
            "company_name": (
                company_name.strip()
                or None
            ),
            "description": description.strip(),
            "source": "manual",
        }

        try:

            response = requests.post(
                f"{API_URL}/job-descriptions/",
                json=payload,
                headers=get_headers(token),
                timeout=30,
            )

            if response.status_code == 401:

                handle_unauthorized()
                return

            if response.status_code in (
                200,
                201,
            ):

                st.success(
                    "Job description saved successfully."
                )

                st.rerun()

            else:

                st.error(
                    get_error_message(
                        response,
                        "Unable to save job description.",
                    )
                )

        except requests.RequestException as error:

            show_connection_error(error)

    st.divider()

    st.subheader(
        "Saved Job Descriptions"
    )

    try:

        response = requests.get(
            f"{API_URL}/job-descriptions/",
            headers=get_headers(token),
            timeout=30,
        )

        if response.status_code == 401:

            handle_unauthorized()
            return

        if response.status_code != 200:

            st.error(
                get_error_message(
                    response,
                    "Unable to load job descriptions.",
                )
            )

            return

        jobs = response.json()

        if not jobs:

            st.info(
                "No job descriptions saved yet."
            )

            return

        for job in jobs:

            with st.container():

                st.markdown(
                    f"### 💼 "
                    f"{job.get('title', 'Job Description')}"
                )

                if job.get(
                    "company_name"
                ):

                    st.write(
                        f"**Company:** "
                        f"{job['company_name']}"
                    )

                st.write(
                    job.get(
                        "description",
                        "",
                    )
                )

                st.caption(
                    f"Source: "
                    f"{job.get('source', 'manual')}"
                )

                st.divider()

    except requests.RequestException as error:

        show_connection_error(error)


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    initialize_session()

    token = st.session_state.get(
        "access_token"
    )

    # --------------------------------------------------------
    # Authentication
    # --------------------------------------------------------

    if not token:

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
    # Verify User
    # --------------------------------------------------------

    user = st.session_state.get(
        "user"
    )

    if user is None:

        try:

            response = get_current_user(
                token
            )

            if response.status_code == 200:

                st.session_state[
                    "user"
                ] = response.json()

                user = st.session_state[
                    "user"
                ]

            elif response.status_code == 401:

                handle_unauthorized()
                return

            else:

                st.error(
                    get_error_message(
                        response,
                        "Unable to verify session.",
                    )
                )

                return

        except requests.RequestException as error:

            show_connection_error(error)
            return

    # --------------------------------------------------------
    # Sidebar
    # --------------------------------------------------------

    with st.sidebar:

        st.title(
            "🎓 Placement AI"
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
                "Readiness Analysis",
                "Job Description",
            ],
        )

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True,
        ):

            logout()

    # --------------------------------------------------------
    # Routing
    # --------------------------------------------------------

    if page == "Dashboard":

        dashboard_page()

    elif page == "Profile":

        profile_page(
            token
        )

    elif page == "Resume":

        resumes_page(
            token
        )

    elif page == "Readiness Analysis":

        readiness_page(
            token
        )

    elif page == "Job Description":

        job_description_page(
            token
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()