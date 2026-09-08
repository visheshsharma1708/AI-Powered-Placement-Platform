from types import SimpleNamespace

from app.ml.feature_engineering import build_readiness_features


analysis = SimpleNamespace(
    skills=[
        "python",
        "sql",
        "aws",
        "fastapi",
    ],
    technologies=[
        "python",
        "postgresql",
        "docker",
    ],
    projects=[
        "Placement Intelligence Platform",
        "Machine Learning Project",
    ],
    experience=[
        "Machine Learning Intern",
    ],
    certifications=[
        "AWS Certification",
    ],
    achievements=[
        "Coding Competition",
    ],
    education=[
        "B.Tech Computer Science",
    ],
    raw_text="Sample resume text " * 100,
)


profile = SimpleNamespace(
    github_url="https://github.com/example",
    linkedin_url="https://linkedin.com/in/example",
    portfolio_url=None,
)


features = build_readiness_features(
    analysis=analysis,
    profile=profile,
)


print("\n===== READINESS FEATURES =====")

for name, value in features.items():
    print(f"{name}: {value}")