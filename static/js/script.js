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
                'input[type="file"]'
            );

        if (fileInput) {

            fileInput.addEventListener(
                "change",
                function () {

                    if (
                        this.files &&
                        this.files.length > 0
                    ) {

                        const file =
                            this.files[0];

                        console.log(
                            "Selected:",
                            file.name
                        );
                    }

                }
            );
        }

    }
);