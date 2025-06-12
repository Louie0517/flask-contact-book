const search_input = document.getElementById("search-input")
const search_form = document.getElementById("search-form")

search_input.addEventListener("input", () => {
    if (search_input.value === "") {
        search_form.submit();
    }
});

window.onload = function() {
    const loginFailed = document.body.getAttribute("data-login-failed") === "true";
    const resetSuccess = document.body.getAttribute("data--reset-success") === "true";

    if(loginFailed) {
        alert("Invalid email or password!")
    }
    if(resetSuccess){
        alert("Reset passsword successfuly!")
    }
}

function displayFileName() {
    const fileInput = document.getElementById("image");
    const fileNameDisplay = document.getElementById("file-name");

    if(fileInput.files.length > 0) {
        fileNameDisplay.textContent = fileInput.files[0].name;
    } else {
        fileNameDisplay.textContent = "No file chosen"
    }
}
