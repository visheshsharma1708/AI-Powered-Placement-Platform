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
    ],
    technologies=[
        "Python",
        "FastAPI",
        "AWS",
        "Docker",
    ],
    projects=[
        "Placement Intelligence Platform",
        "Machine Learning Project",
    ],
    experience=[
        "Machine Learning Internship",
    ],
    certifications=[
        "AWS Certification",
    ],
    achievements=[
        "Coding Achievement",
    ],
    education=[
        "B.Tech Computer Science",
    ],
    raw_text="Python machine learning AWS FastAPI " * 100,
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


print("\n========== READINESS ==========")

print(
    "Prediction:",
    result["prediction"],
)

print(
    "Probability:",
    result["readiness_probability"],
)

print(
    "Score:",
    result["readiness_score"],
)


print("\n========== POSITIVE FACTORS ==========")

for item in result["explanation"]["positive_factors"]:
    print(
        f"{item['label']}: "
        f"{item['contribution']}"
    )


print("\n========== IMPROVEMENT AREAS ==========")

for item in result["explanation"]["improvement_areas"]:
    print(
        f"{item['label']}: "
        f"{item['contribution']}"
    )