import httpx
import streamlit as st


BACKEND_URL = "http://127.0.0.1:8000"


def check_backend_health():
    """
    Calls the FastAPI health endpoint and returns
    the backend connection status.
    """
    try:
        response = httpx.get(
            f"{BACKEND_URL}/health",
            timeout=5.0,
        )

        if response.status_code == 200:
            return True, response.json()

        return False, {
            "message": "Backend returned an unexpected response."
        }

    except httpx.RequestError:
        return False, {
            "message": "Unable to connect to the backend."
        }


st.set_page_config(
    page_title="Placement Intelligence Platform",
    page_icon="🎓",
    layout="wide",
)


backend_is_healthy, backend_data = check_backend_health()


st.title("🎓 Placement Intelligence & Career Readiness Platform")

st.write(
    """
    An AI-powered platform for resume analysis, career readiness estimation,
    skill gap analysis, job matching, and personalized career intelligence.
    """
)

st.divider()

st.subheader("System Status")

col1, col2, col3 = st.columns(3)


with col1:
    if backend_is_healthy:
        st.metric(
            label="Backend",
            value="Healthy",
        )
    else:
        st.metric(
            label="Backend",
            value="Unavailable",
        )


with col2:
    st.metric(
        label="ML Engine",
        value="Coming Soon",
    )


with col3:
    st.metric(
        label="AI Engine",
        value="Coming Soon",
    )


if backend_is_healthy:
    st.success(
        "FastAPI backend is connected successfully."
    )
else:
    st.error(
        "Unable to connect to the FastAPI backend. "
        "Make sure the backend server is running."
    )

    st.code(
        "uvicorn app.main:app --reload --app-dir backend",
        language="bash",
    )


with st.expander("View Backend Response"):
    st.json(backend_data)