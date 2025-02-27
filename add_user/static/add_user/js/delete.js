document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-form").forEach(form => {
        form.addEventListener("submit", function (event) {
            let confirmDelete = confirm("Are you sure you want to delete this item?");
            if (!confirmDelete) {
                event.preventDefault(); // Prevent form submission if user cancels
            }
        });
    });
});
