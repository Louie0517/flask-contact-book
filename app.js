const search_input = document.getElementById("search-input")
const search_form = document.getElementById("search-form")

search_input.addEventListener("input", () => {
    if (search_input.value === "") {
        search_form.submit();
    }
});