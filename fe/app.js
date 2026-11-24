const loginForm = document.getElementById("loginForm");

loginForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const message = document.getElementById("message");

    const formData = new URLSearchParams();

    formData.append("username", username);
    formData.append("password", password);

    try {

        const response = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",

            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },

            body: formData
        });

        const data = await response.json();

        if (response.ok) {

            localStorage.setItem("token", data.access_token);
            

            message.textContent = "Login successful!";
            window.location.href = "dashboard.html";

            console.log("JWT Token:", data.access_token);

        } else {

            message.textContent = data.detail;

        }

    } catch (error) {

        message.textContent = "Unable to connect to server.";
        console.error(error);

    }
});