import streamlit as st

from api_client import (
    create_profile,
    get_profile,
    update_profile,
)


def show_profile_page():

    st.title("👤 Student Profile")

    token = st.session_state.get("access_token")

    if not token:
        st.warning("Please login first.")
        return

    try:
        response = get_profile(token)

        if response.status_code == 200:
            profile = response.json()
            profile_exists = True

        elif response.status_code == 404:
            profile = {}
            profile_exists = False

        elif response.status_code == 401:
            st.error("Your session has expired. Please login again.")
            return

        else:
            st.error(
                f"Unable to load profile: {response.text}"
            )
            return

    except Exception as error:
        st.error(
            f"Unable to connect to backend: {error}"
        )
        return

    if profile_exists:
        st.success("Your profile is currently saved.")
    else:
        st.info(
            "Your profile has not been created yet. "
            "Complete the form below."
        )

    with st.form("student_profile_form"):

        university = st.text_input(
            "University",
            value=profile.get("university", ""),
            placeholder="Example: University of Rajasthan",
        )

        degree = st.text_input(
            "Degree",
            value=profile.get("degree", ""),
            placeholder="Example: B.Tech",
        )

        branch = st.text_input(
            "Branch / Specialization",
            value=profile.get("branch", ""),
            placeholder="Example: Computer Science and Engineering",
        )

        graduation_year = st.number_input(
            "Graduation Year",
            min_value=2000,
            max_value=2100,
            value=(
                profile.get("graduation_year")
                if profile.get("graduation_year")
                else 2026
            ),
            step=1,
        )

        target_role = st.text_input(
            "Target Job Role",
            value=profile.get("target_role", ""),
            placeholder="Example: Machine Learning Engineer",
        )

        github_url = st.text_input(
            "GitHub URL",
            value=profile.get("github_url", ""),
            placeholder="https://github.com/username",
        )

        linkedin_url = st.text_input(
            "LinkedIn URL",
            value=profile.get("linkedin_url", ""),
            placeholder="https://www.linkedin.com/in/username",
        )

        portfolio_url = st.text_input(
            "Portfolio URL",
            value=profile.get("portfolio_url", ""),
            placeholder="https://yourportfolio.com",
        )

        bio = st.text_area(
            "Professional Bio",
            value=profile.get("bio", ""),
            placeholder=(
                "Briefly describe your technical interests, "
                "experience, and career goals."
            ),
            height=150,
        )

        submitted = st.form_submit_button(
            "Save Profile",
            use_container_width=True,
        )

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

            if response.status_code in (200, 201):

                st.success(
                    "Profile saved successfully."
                )

                st.rerun()

            elif response.status_code == 409:

                st.warning(
                    "A profile already exists for this account."
                )

            elif response.status_code == 401:

                st.error(
                    "Your session has expired. Please login again."
                )

            elif response.status_code == 422:

                st.error(
                    "Some information is invalid. "
                    "Please check the entered values."
                )

            else:

                st.error(
                    f"Unable to save profile: {response.text}"
                )

        except Exception as error:

            st.error(
                f"Unable to connect to backend: {error}"
            )