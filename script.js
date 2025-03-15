import  { db, ref, get } from "./db.js";  // Correct relative path
function User_Login() {
    var usern = document.getElementById('username').value.trim();
    var passw = document.getElementById('password').value.trim();

    get(ref(db, 'user/' + usern)).then((snapshot) => {
        const data = snapshot.val();
        if (data && data['password'] == passw) {
            localStorage.setItem('loggedOut', true);
            window.location.replace("home.html");
        } else {
            alert("Invalid credentials, please try again.");
            location.reload();
        }
    }).catch((error) => {
        alert("Login failed. Please try again.");
        console.error(error);
    });
}

window.onload = function () {
    const loginForm = document.getElementById("Login-form");
    loginForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent form submission
        User_Login();
    });
};
