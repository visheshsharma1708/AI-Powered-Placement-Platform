import httpx


BACKEND_URL = "http://127.0.0.1:8000"


def register_user(
    email: str,
    full_name: str,
    password: str,
):
    return httpx.post(
        f"{BACKEND_URL}/auth/register",
        json={
            "email": email,
            "full_name": full_name,
            "password": password,
        },
        timeout=10.0,
    )


def login_user(
    email: str,
    password: str,
):
    return httpx.post(
        f"{BACKEND_URL}/auth/login",
        json={
            "email": email,
            "password": password,
        },
        timeout=10.0,
    )


def get_current_user(token: str):
    return httpx.get(
        f"{BACKEND_URL}/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
        timeout=10.0,
    )


def get_profile(token: str):
    return httpx.get(
        f"{BACKEND_URL}/profiles/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
        timeout=10.0,
    )


def create_profile(
    token: str,
    profile_data: dict,
):
    return httpx.post(
        f"{BACKEND_URL}/profiles/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=profile_data,
        timeout=10.0,
    )


def update_profile(
    token: str,
    profile_data: dict,
):
    return httpx.put(
        f"{BACKEND_URL}/profiles/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=profile_data,
        timeout=10.0,
    )