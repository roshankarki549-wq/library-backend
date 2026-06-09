document
    .getElementById("loadBtn")
    .addEventListener("click", loadBooks);

function loadBooks() {

    fetch("http://127.0.0.1:8000/api/books/")

        .then(response => response.json())

        .then(data => {

            const bookList =
                document.getElementById("bookList");

            bookList.innerHTML = "";

            data.forEach(book => {

                const li =
                    document.createElement("li");

                li.textContent =
                    `${book.title} - ${book.author}`;

                bookList.appendChild(li);

            });

        })

        .catch(error => {

            console.error(
                "Error:",
                error
            );

        });
}