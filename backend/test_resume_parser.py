from app.services.resume_parser import analyze_resume


sample_resume = """
Vishesh Sharma

EDUCATION

B.Tech Computer Science
ABC University
2027

TECHNICAL SKILLS

Python, SQL, PostgreSQL, FastAPI, AWS, Docker, Machine Learning

PROJECTS

Placement Intelligence Platform
Built a career readiness platform using Python, FastAPI and PostgreSQL.

EXPERIENCE

Machine Learning Intern
Worked on machine learning models and AWS services.

CERTIFICATIONS

AWS Cloud Certification

ACHIEVEMENTS

Solved multiple programming problems and participated in coding competitions.
"""


result = analyze_resume(sample_resume)


print("\n===== RESUME ANALYSIS =====")

print("\nSkills:")
print(result["skills"])

print("\nEducation:")
print(result["education"])

print("\nProjects:")
print(result["projects"])

print("\nExperience:")
print(result["experience"])

print("\nCertifications:")
print(result["certifications"])

print("\nAchievements:")
print(result["achievements"])

print("\nTechnologies:")
print(result["technologies"])