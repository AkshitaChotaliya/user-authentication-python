function submitLogin() {
     const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const usernameOrEmail = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const data = {
        username_or_email: usernameOrEmail,
        password: password
    };

    fetch("/api/auth/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json().then(data => ({ ok: response.ok, data })))
    .then(({ ok, data }) => {
        const messageBox = document.getElementById("responseMessage");
        if (ok) {
            messageBox.textContent = "Login successful!";
            messageBox.classList.remove("text-red-500");
            messageBox.classList.add("text-green-600");

            localStorage.setItem("authToken", data.token);

            setTimeout(() => {
                window.location.href = "/dashboard/";
            }, 1000);
        } else {
            messageBox.textContent = data.detail || "Login failed.";
            messageBox.classList.remove("text-green-600");
            messageBox.classList.add("text-red-500");
        }
    })
    .catch(error => {
        const messageBox = document.getElementById("responseMessage");
        messageBox.textContent = "Something went wrong.";
        messageBox.classList.remove("text-green-600");
        messageBox.classList.add("text-red-500");
        console.error("Login Error:", error);
    });


}
