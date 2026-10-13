document.addEventListener(
    "DOMContentLoaded",
    function () {

        const currentPath =
            window.location.pathname;

        document
            .querySelectorAll(".nav-links a")
            .forEach(function (link) {

                if (
                    link.getAttribute("href") ===
                    currentPath
                ) {

                    link.classList.add(
                        "active"
                    );
                }

            });


        const fileInput =
            document.querySelector(
                '#dataset-file'
            );

        if (fileInput) {
            const dropzone =
                document.querySelector("#dropzone");
            const fileStatus =
                document.querySelector("#file-status");

            function updateSelectedFile() {
                const file = fileInput.files[0];

                if (!file) {
                    return;
                }

                if (!/\.(csv|xlsx)$/i.test(file.name)) {
                    fileInput.value = "";
                    fileStatus.textContent =
                        "Choose a CSV or XLSX file";
                    dropzone.classList.remove("is-selected");
                    return;
                }

                fileStatus.textContent = file.name;
                dropzone.classList.add("is-selected");
            }

            fileInput.addEventListener(
                "change",
                updateSelectedFile
            );

            ["dragenter", "dragover"].forEach(function (eventName) {
                dropzone.addEventListener(eventName, function (event) {
                    event.preventDefault();
                    dropzone.classList.add("is-dragging");
                });
            });

            ["dragleave", "drop"].forEach(function (eventName) {
                dropzone.addEventListener(eventName, function (event) {
                    event.preventDefault();
                    dropzone.classList.remove("is-dragging");
                });
            });

            dropzone.addEventListener("drop", function (event) {
                if (event.dataTransfer.files.length) {
                    fileInput.files = event.dataTransfer.files;
                    updateSelectedFile();
                }
            });
        }

    }
);