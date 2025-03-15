//import { db, ref, get } from "./db.js";
function Logout_fun() {
    // Clear local storage and session storage
    localStorage.clear();
    sessionStorage.clear();

    // Clear cookies
    document.cookie.split(";").forEach((c) => {
        document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
    });

    // Prevent back navigation after logout
    history.pushState(null, null, location.href);
    window.onpopstate = function () {
        history.go(1);
    };

    // Redirect to login page
    window.location.replace("index.html");
}
