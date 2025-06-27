document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("signupForm");
    if (form) {
        form.addEventListener("submit", async function (event) {
           console.log("Form submitted");
           event.preventDefault();
               const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                const username = document.getElementById("username").value;
                const email = document.getElementById("email").value;
                const password = document.getElementById("password").value;

                const data = {username, email, password};

                console.log(csrfToken,"<---- csrfToken --->");
                try {
                    const response = await fetch("/api/auth/signup/",{
                        method:"POST",
                        headers:{
                             "Content-Type": "application/json",
                             "X-CSRFToken": csrfToken
                        },
                        body: JSON.stringify(data)                  
                    });
                    console.log(response,"<--- response --->");
                    
                    const result = await response.json();
                    console.log("<--- result --->", result);

                    document.getElementById("responseMessage").textContent = result.message || "Signup successful.";
                    document.getElementById("responseMessage").classList.remove("text-red-500");
                    document.getElementById("responseMessage").classList.add("text-green-600");
                    
                } catch (error) {
                    document.getElementById("responseMessage").textContent = "Something went wrong.";
                    document.getElementById("responseMessage").classList.remove("text-green-600");
                    document.getElementById("responseMessage").classList.add("text-red-500");
                    console.error("Signup Error:", error);
                }
                
        });
    }
});