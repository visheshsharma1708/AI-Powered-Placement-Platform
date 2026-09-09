import streamlit as st

from api_client import (
    create_profile,
    get_profile,
    update_profile,
)


st.set_page_config(
    page_title="Student Profile",
    page_icon="👤",
    layout="wide",
)


def show_profile_page():

    st.title("👤 Student Profile")
    st.write("Complete your profile to improve your placement readiness.")

    # ============================================================
    # CHECK LOGIN
    # ============================================================

    token = st.session_state.get("access_token")

    if not token:
        st.warning("Please login first.")
        st.stop()

    # ============================================================
    # LOAD PROFILE
    # ============================================================

    profile = {}
    profile_exists = False

    try:

        response = get_profile(token)

        if response.status_code == 200:

            profile = response.json()

            if not isinstance(profile, dict):
                profile = {}

            profile_exists = True

        elif response.status_code == 404:

            profile = {}
            profile_exists = False

        elif response.status_code == 401:

            st.error(
                "Your session has expired. Please login again."
            )

            st.session_state.pop("access_token", None)
            st.stop()

        else:

            st.error(
                f"Unable to load profile. "
                f"Status code: {response.status_code}"
            )

            st.code(response.text)

            st.stop()

    except Exception as error:

        st.error(
            "Unable to connect to the backend."
        )

        st.exception(error)

        st.stop()

    # ============================================================
    # PROFILE STATUS
    # ============================================================

    if profile_exists:

        st.success(
            "Your profile is currently saved."
        )

    else:

        st.info(
            "Your profile has not been created yet. "
            "Complete the form below."
        )

    st.divider()

    # ============================================================
    # PROFILE FORM
    # ============================================================

    with st.form("student_profile_form"):

        st.subheader("🎓 Academic Information")

        university = st.text_input(
            "University",
            value=profile.get("university") or "",
            placeholder="Example: University of Rajasthan",
        )

        degree = st.text_input(
            "Degree",
            value=profile.get("degree") or "",
            placeholder="Example: B.Tech",
        )

        branch = st.text_input(
            "Branch / Specialization",
            value=profile.get("branch") or "",
            placeholder="Example: Computer Science and Engineering",
        )

        graduation_year = st.number_input(
            "Graduation Year",
            min_value=2000,
            max_value=2100,
            value=int(
                profile.get("graduation_year")
                or 2026
            ),
            step=1,
        )

        st.divider()

        st.subheader("💼 Career Information")

        target_role = st.text_input(
            "Target Job Role",
            value=profile.get("target_role") or "",
            placeholder="Example: Machine Learning Engineer",
        )

        st.divider()

        st.subheader("🔗 Professional Links")

        github_url = st.text_input(
            "GitHub URL",
            value=profile.get("github_url") or "",
            placeholder="https://github.com/username",
        )

        linkedin_url = st.text_input(
            "LinkedIn URL",
            value=profile.get("linkedin_url") or "",
            placeholder="https://www.linkedin.com/in/username",
        )

        portfolio_url = st.text_input(
            "Portfolio URL",
            value=profile.get("portfolio_url") or "",
            placeholder="https://yourportfolio.com",
        )

        st.divider()

        st.subheader("📝 Professional Summary")

        bio = st.text_area(
            "Professional Bio",
            value=profile.get("bio") or "",
            placeholder=(
                "Briefly describe your technical interests, "
                "experience, skills, projects, and career goals."
            ),
            height=150,
        )

        submitted = st.form_submit_button(
            "💾 Save Profile",
            use_container_width=True,
        )

    # ============================================================
    # SAVE PROFILE
    # ============================================================

    if submitted:

        profile_data = {
            "university": university.strip() or None,
            "degree": degree.strip() or None,
            "branch": branch.strip() or None,
            "graduation_year": int(graduation_year),
            "target_role": target_role.strip() or None,
            "github_url": github_url.strip() or None,
            "linkedin_url": linkedin_url.strip() or None,
            "portfolio_url": portfolio_url.strip() or None,
            "bio": bio.strip() or None,
        }

        try:

            if profile_exists:

                response = update_profile(
                    token,
                    profile_data,
                )

            else:

                response = create_profile(
                    token,
                    profile_data,
                )

            # ====================================================
            # SUCCESS
            # ====================================================

            if response.status_code in (200, 201):

                st.success(
                    "✅ Profile saved successfully!"
                )

                st.rerun()

            # ====================================================
            # UNAUTHORIZED
            # ====================================================

            elif response.status_code == 401:

                st.error(
                    "Your session has expired. "
                    "Please login again."
                )

                st.session_state.pop(
                    "access_token",
                    None,
                )

            # ====================================================
            # PROFILE ALREADY EXISTS
            # ====================================================

            elif response.status_code == 409:

                st.warning(
                    "A profile already exists for this account."
                )

                st.info(
                    "Please refresh the page and try updating "
                    "your existing profile."
                )

            # ====================================================
            # VALIDATION ERROR
            # ====================================================

            elif response.status_code == 422:

                st.error(
                    "Some information is invalid. "
                    "Please check the entered values."
                )

                st.code(response.text)

            # ====================================================
            # NOT FOUND
            # ====================================================

            elif response.status_code == 404:

                st.error(
                    "The profile API endpoint was not found."
                )

                st.code(response.text)

            # ====================================================
            # OTHER BACKEND ERROR
            # ====================================================

            else:

                st.error(
                    f"Unable to save profile. "
                    f"Status code: {response.status_code}"
                )

                st.code(response.text)

        except Exception as error:

            st.error(
                "Unable to connect to the backend."
            )

            st.exception(error)


# ================================================================
# IMPORTANT:
# STREAMLIT PAGES ARE EXECUTED DIRECTLY.
# CALL THE FUNCTION HERE.
# ================================================================

show_profile_page()