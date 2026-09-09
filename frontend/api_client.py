import httpx


# ============================================================
# BACKEND CONFIGURATION
# ============================================================

BACKEND_URL = "http://127.0.0.1:8000"

DEFAULT_TIMEOUT = 30.0
UPLOAD_TIMEOUT = 60.0
ANALYSIS_TIMEOUT = 120.0


# ============================================================
# COMMON HELPERS
# ============================================================

def get_auth_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }


# ============================================================
# AUTHENTICATION
# ============================================================

def register_user(
    email: str,
    full_name: str,
    password: str,
):
    return httpx.post(
        f"{BACKEND_URL}/auth/register",
        json={
            "email": email.strip(),
            "full_name": full_name.strip(),
            "password": password,
        },
        timeout=DEFAULT_TIMEOUT,
    )


def login_user(
    email: str,
    password: str,
):
    return httpx.post(
        f"{BACKEND_URL}/auth/login",
        json={
            "email": email.strip(),
            "password": password,
        },
        timeout=DEFAULT_TIMEOUT,
    )


def get_current_user(
    token: str,
):
    return httpx.get(
        f"{BACKEND_URL}/users/me",
        headers=get_auth_headers(token),
        timeout=DEFAULT_TIMEOUT,
    )


# ============================================================
# STUDENT PROFILE
# ============================================================

def get_profile(
    token: str,
):
    return httpx.get(
        f"{BACKEND_URL}/profiles/me",
        headers=get_auth_headers(token),
        timeout=DEFAULT_TIMEOUT,
    )


def create_profile(
    token: str,
    profile_data: dict,
):
    return httpx.post(
        f"{BACKEND_URL}/profiles/me",
        headers=get_auth_headers(token),
        json=profile_data,
        timeout=DEFAULT_TIMEOUT,
    )


def update_profile(
    token: str,
    profile_data: dict,
):
    return httpx.put(
        f"{BACKEND_URL}/profiles/me",
        headers=get_auth_headers(token),
        json=profile_data,
        timeout=DEFAULT_TIMEOUT,
    )


# ============================================================
# RESUME MANAGEMENT
# ============================================================

def get_resumes(
    token: str,
):
    return httpx.get(
        f"{BACKEND_URL}/resumes/",
        headers=get_auth_headers(token),
        timeout=DEFAULT_TIMEOUT,
    )


def upload_resume(
    token: str,
    file_name: str,
    file_content: bytes,
    content_type: str = "application/pdf",
):
    files = {
        "file": (
            file_name,
            file_content,
            content_type,
        )
    }

    return httpx.post(
        f"{BACKEND_URL}/resumes/upload",
        headers=get_auth_headers(token),
        files=files,
        timeout=UPLOAD_TIMEOUT,
    )


def analyze_resume(
    token: str,
    resume_id: int,
):
    return httpx.post(
        f"{BACKEND_URL}/resumes/{resume_id}/analyze",
        headers=get_auth_headers(token),
        timeout=ANALYSIS_TIMEOUT,
    )


def download_resume(
    token: str,
    resume_id: int,
):
    return httpx.get(
        f"{BACKEND_URL}/resumes/{resume_id}/download",
        headers=get_auth_headers(token),
        timeout=UPLOAD_TIMEOUT,
    )


# ============================================================
# PLACEMENT READINESS
# ============================================================

def predict_readiness(
    token: str,
    resume_id: int,
):
    return httpx.post(
        f"{BACKEND_URL}/readiness/{resume_id}/predict",
        headers=get_auth_headers(token),
        timeout=ANALYSIS_TIMEOUT,
    )


# ============================================================
# JOB DESCRIPTIONS
# ============================================================

def create_job_description(
    token: str,
    job_data: dict,
):
    return httpx.post(
        f"{BACKEND_URL}/job-descriptions/",
        headers=get_auth_headers(token),
        json=job_data,
        timeout=DEFAULT_TIMEOUT,
    )


def get_job_descriptions(
    token: str,
):
    return httpx.get(
        f"{BACKEND_URL}/job-descriptions/",
        headers=get_auth_headers(token),
        timeout=DEFAULT_TIMEOUT,
    )


# ============================================================
# JOB MATCHING
# ============================================================

def match_resume_with_job(
    token: str,
    resume_id: int,
    job_id: int,
):
    return httpx.post(
        f"{BACKEND_URL}/job-matching/",
        headers=get_auth_headers(token),
        json={
            "resume_id": resume_id,
            "job_id": job_id,
        },
        timeout=ANALYSIS_TIMEOUT,
    )