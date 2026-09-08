from types import SimpleNamespace

from app.ml.prediction_service import predict_readiness


analysis = SimpleNamespace(
    skills=[
        "Python",
        "SQL",
        "Machine Learning",
        "FastAPI",
        "AWS",
        "Docker",
        "PostgreSQL",
        "Git",
        "Pandas",
        "NumPy",
    ],
    technologies=[
        "Python",
        "PostgreSQL",
        "FastAPI",
        "Docker",
        "AWS",
    ],
    projects=[
        "Placement Intelligence Platform",
        "Machine Learning Project",
        "Data Analysis Project",
        "Web Application",
    ],
    experience=[
        "Machine Learning Intern",
    ],
    certifications=[
        "AWS Certification",
        "Machine Learning Certification",
    ],
    achievements=[
        "Coding Competition",
        "Academic Achievement",
    ],
    education=[
        "B.Tech Computer Science",
    ],
    raw_text="Sample resume text " * 150,
)


profile = SimpleNamespace(
    github_url="https://github.com/example",
    linkedin_url="https://linkedin.com/in/example",
    portfolio_url="https://example.com",
)


result = predict_readiness(
    analysis=analysis,
    profile=profile,
)


print("\n===== READINESS PREDICTION =====")

print(
    f"Prediction: "
    f"{result['prediction']}"
)

print(
    f"Probability: "
    f"{result['readiness_probability']}"
)

print(
    f"Readiness Score: "
    f"{result['readiness_score']}%"
)

print("\n===== FEATURES =====")

for name, value in result["features"].items():
    print(f"{name}: {value}")