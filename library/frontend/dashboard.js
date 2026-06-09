const BASE_URL = "http://127.0.0.1:8000/api/dashboard";

function loadDashboard() {

    loadStats();

    loadRecentIssues();

    loadPopularBooks();

    loadNotifications();
}


// ====================
// Dashboard Stats
// ====================

function loadStats() {

    fetch(`${BASE_URL}/stats/`)

        .then(response => response.json())

        .then(data => {

            document.getElementById("totalBooks").innerText =
                data.total_books;

            document.getElementById("totalMembers").innerText =
                data.total_members;

            document.getElementById("booksIssued").innerText =
                data.books_issued;

            document.getElementById("overdueBooks").innerText =
                data.overdue_books;
        })

        .catch(error => console.log(error));
}


// ====================
// Recent Issues
// ====================

function loadRecentIssues() {

    fetch(`${BASE_URL}/recent-issues/`)

        .then(response => response.json())

        .then(data => {

            const list =
                document.getElementById("recentIssues");

            list.innerHTML = "";

            data.forEach(issue => {

                const li =
                    document.createElement("li");

                li.innerHTML = `
                    <b>${issue.book}</b>
                    <br>
                    Member:
                    ${issue.member}
                `;

                list.appendChild(li);

            });

        })

        .catch(error => console.log(error));
}


// ====================
// Popular Books
// ====================

function loadPopularBooks() {

    fetch(`${BASE_URL}/popular-books/`)

        .then(response => response.json())

        .then(data => {

            const container =
                document.getElementById("popularBooks");

            container.innerHTML = "";

            data.forEach(book => {

                const div =
                    document.createElement("div");

                div.style.border =
                    "1px solid gray";

                div.style.margin =
                    "10px";

                div.style.padding =
                    "10px";

                div.innerHTML = `

              <img
                src="http://127.0.0.1:8000${book.cover_image}"
                width="80"
            >

            <h3>${book.title}</h3>

            <p>${book.author}</p>

            <p>Issued ${book.times_issued} times</p>
        `;

                container.appendChild(div);

            });

        })

        .catch(error => console.log(error));
}

function loadNotifications() {

    fetch(
        "http://127.0.0.1:8000/api/dashboard/notifications/"
    )

    .then(response => response.json())

    .then(data => {

        const list =
            document.getElementById(
                "notifications"
            );

        list.innerHTML = "";

        data.forEach(item => {

            const li =
                document.createElement("li");

           li.innerText =
            `${item.date} | [${item.type.toUpperCase()}] ${item.message}`;
            list.appendChild(li);

        });

    })

    .catch(error =>
        console.log(error)
    );
}