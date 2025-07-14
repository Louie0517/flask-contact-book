function imageAddress() {
    const fileInput = document.getElementById("fileImg");
    const fileLabel = document.getElementById("fileName");

    fileInput.addEventListener("change", () => {
        if(fileInput.files.length > 0) {
            fileLabel.textContent = fileInput.files[0].name;
        }
        else {
            fileLabel.textContent = "Insert image"
        }
    });
}

imageAddress()