function launchApp() {
    window.open(
        "http://localhost:8501",
        "_blank"
    );
}

function scrollToServices() {
    document.querySelector(".services").scrollIntoView({
        behavior: "smooth"
    });
}