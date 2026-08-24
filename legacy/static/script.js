document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form");
    const button = document.getElementById("predictBtn");

    if (!form) return;

    function showToast(message, type = "danger") {

        let oldToast = document.getElementById("customToast");

        if (oldToast) oldToast.remove();

        const toast = document.createElement("div");

        toast.id = "customToast";
        toast.className = `alert alert-${type} shadow`;

        toast.style.position = "fixed";
        toast.style.top = "20px";
        toast.style.right = "20px";
        toast.style.zIndex = "9999";
        toast.style.minWidth = "320px";
        toast.style.borderRadius = "12px";

        toast.innerHTML = `<strong>${message}</strong>`;

        document.body.appendChild(toast);

        setTimeout(() => {

            toast.remove();

        }, 3000);

    }

    document.querySelectorAll(".form-control,.form-select").forEach(input => {

        input.addEventListener("focus", () => {

            input.style.transform = "scale(1.02)";

        });

        input.addEventListener("blur", () => {

            input.style.transform = "scale(1)";

        });

    });

    form.addEventListener("submit", function (e) {

        const cgpa = parseFloat(document.querySelector("[name='cgpa']").value);
        const dsa = parseInt(document.querySelector("[name='dsa']").value);
        const projects = parseInt(document.querySelector("[name='projects']").value);
        const communication = parseInt(document.querySelector("[name='communication']").value);
        const resume = document.querySelector("[name='resume']").files[0];

        if (cgpa < 0 || cgpa > 10) {

            e.preventDefault();

            showToast("CGPA must be between 0 and 10.");

            return;

        }

        if (dsa < 0 || dsa > 100) {

            e.preventDefault();

            showToast("DSA Score must be between 0 and 100.");

            return;

        }

        if (projects < 0 || projects > 20) {

            e.preventDefault();

            showToast("Projects should be between 0 and 20.");

            return;

        }

        if (communication < 1 || communication > 10) {

            e.preventDefault();

            showToast("Communication Skills must be between 1 and 10.");

            return;

        }

        if (resume) {

            const extension = resume.name.split(".").pop().toLowerCase();

            if (extension !== "pdf") {

                e.preventDefault();

                showToast("Only PDF Resume is allowed.");

                return;

            }

            if (resume.size > 5 * 1024 * 1024) {

                e.preventDefault();

                showToast("Resume must be smaller than 5 MB.");

                return;

            }

        }

        button.disabled = true;

        button.innerHTML = `
        <span class="spinner-border spinner-border-sm me-2"></span>
        Predicting...
        `;

        const overlay = document.createElement("div");

        overlay.id = "loadingOverlay";

        overlay.style.position = "fixed";
        overlay.style.left = "0";
        overlay.style.top = "0";
        overlay.style.width = "100%";
        overlay.style.height = "100%";
        overlay.style.background = "rgba(255,255,255,0.85)";
        overlay.style.display = "flex";
        overlay.style.flexDirection = "column";
        overlay.style.justifyContent = "center";
        overlay.style.alignItems = "center";
        overlay.style.zIndex = "9998";

        overlay.innerHTML = `
            <div class="spinner-border text-primary" style="width:4rem;height:4rem;"></div>
            <h3 class="mt-4">Predicting Placement...</h3>
            <p>Machine Learning model is analysing student profile.</p>
        `;

        document.body.appendChild(overlay);

    });

});