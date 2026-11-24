const token = localStorage.getItem("token");

if (!token) {
    window.location.href = "index.html";
}


async function getAverageGrade() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/analytics/average-grade",
            {
                method: "GET",

                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const data = await response.json();

        if (!response.ok) {

            console.log(data);
            return;

        }

document.getElementById("averageGrade").textContent =
    data.average_final_grade;

    } catch (error) {

        console.error(error);

        document.getElementById("averageGrade").textContent =
            "Unable to connect to server.";

    }
}


getAverageGrade();
getTopStudents();
getSchoolStats();
getAbsenceStats();
async function getTopStudents() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/analytics/top-students",
            {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const data = await response.json();

        if (!response.ok) {
            console.log(data);
            return;
        }

let table = `
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>School</th>
                <th>Gender</th>
                <th>Age</th>
                <th>Grade 1</th>
                <th>Grade 2</th>
                <th>Final Grade</th>
            </tr>
        </thead>

        <tbody>
`;

data.forEach(student => {

    table += `
        <tr>
            <td>${student.id}</td>
            <td>${student.school}</td>
            <td>${student.gender}</td>
            <td>${student.age}</td>
            <td>${student.grade_1}</td>
            <td>${student.grade_2}</td>
            <td>${student.final_grade}</td>
        </tr>
    `;

});

table += `
        </tbody>
    </table>
`;

document.getElementById("topStudents").innerHTML = table;

    } catch (error) {

        console.error(error);

        document.getElementById("topStudents").textContent =
            "Unable to connect to server.";

    }
}


async function getSchoolStats() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/analytics/school-stats",
            {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const data = await response.json();

        if (!response.ok) {
            console.log(data);
            return;
        }

let table = `
    <table>
        <thead>
            <tr>
                <th>School</th>
                <th>Total Students</th>
                <th>Average Grade</th>
            </tr>
        </thead>

        <tbody>
`;

data.forEach(school => {

    table += `
        <tr>
            <td>${school.school}</td>
            <td>${school.total_students}</td>
            <td>${school.average_grade}</td>
        </tr>
    `;

});

table += `
        </tbody>
    </table>
`;

document.getElementById("schoolStats").innerHTML = table;

    } catch (error) {

        console.error(error);

        document.getElementById("schoolStats").textContent =
            "Unable to connect to server.";

    }
}


async function getAbsenceStats() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/analytics/absence-stats",
            {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const data = await response.json();

        if (!response.ok) {
            console.log(data);
            return;
        }

document.getElementById("absenceStats").innerHTML = `

    <div class="absence-grid">

        <div class="stat-box">
            <h3>Minimum Absences</h3>
            <p>${data.minimum_absences}</p>
        </div>

        <div class="stat-box">
            <h3>Maximum Absences</h3>
            <p>${data.maximum_absences}</p>
        </div>

        <div class="stat-box">
            <h3>Average Absences</h3>
            <p>${data.average_absences}</p>
        </div>

        <div class="stat-box">
            <h3>Above 10 Absences</h3>
            <p>${data.students_above_10_absences}</p>
        </div>

    </div>

`;

    } catch (error) {

        console.error(error);

        document.getElementById("absenceStats").textContent =
            "Unable to connect to server.";

    }
}