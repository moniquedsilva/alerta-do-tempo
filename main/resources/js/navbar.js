window.addEventListener("load", function () {
    // Menu mobile
    const nav = document.querySelector(".nav-toggle");
    const links = document.getElementById("links");
    nav.addEventListener("click", function () {
        if (links.style.height === "max-height") {
            links.style.height = "12rem";
        } else {
            links.style.height = "max-height";
        }
    });
});
