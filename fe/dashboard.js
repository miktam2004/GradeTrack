const token = localStorage.getItem("token");
let allStudents = [];
let editingStudentId = null;

if (!token) {
    window.location.href = "index.html";
}

async function getStudents() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/students",
            {
                method: "GET",

                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );
if (response.status === 401) {
    localStorage.removeItem("token");
    window.location.href = "index.html";
    return;
}
        const data = await response.json();

        if (!response.ok) {
            console.log(data);
            return;
        }

allStudents = data;
displayStudents(allStudents);

    } catch (error) {

        console.error(error);

    }
}


function displayStudents(students) {

    const container = document.getElementById("students");

    let table = `
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>School</th>
                    <th>Gender</th>
                    <th>Age</th>
                    <th>Study Time</th>
                    <th>Failures</th>
                    <th>Absences</th>
                    <th>Grade 1</th>
                    <th>Grade 2</th>
                    <th>Final Grade</th>
                    <th>Actions</th>
                </tr>
            </thead>

            <tbody>
    `;

    students.forEach(student => {

        table += `
            <tr>
                <td>${student.id}</td>
                <td>${student.school}</td>
                <td>${student.gender}</td>
                <td>${student.age}</td>
                <td>${student.study_time}</td>
                <td>${student.failures}</td>
                <td>${student.absences}</td>
                <td>${student.grade_1}</td>
                <td>${student.grade_2}</td>
                <td>${student.final_grade}</td>
                <td>
    <button onclick="editStudent(${student.id})">Edit</button>
    <button onclick="deleteStudent(${student.id})">Delete</button>
</td>
            </tr>
        `;

    });

    table += `
            </tbody>
        </table>
    `;

    container.innerHTML = table;
}


getStudents();


document.getElementById("logoutBtn").addEventListener("click", function () {

    localStorage.removeItem("token");

    window.location.href = "index.html";

});

document.getElementById("searchInput").addEventListener("input", function () {

    const searchValue = this.value.toLowerCase();

const filteredStudents = allStudents.filter(student =>
    student.id.toString() === searchValue ||
    student.school.toLowerCase().includes(searchValue)
);


    displayStudents(filteredStudents);

});
document.getElementById("studentForm").addEventListener("submit", async function (event) {

    event.preventDefault();

    const student = {
        school: document.getElementById("school").value,
        gender: document.getElementById("gender").value,
        age: Number(document.getElementById("age").value),
        address: document.getElementById("address").value,
        study_time: Number(document.getElementById("study_time").value),
        failures: Number(document.getElementById("failures").value),
        internet: document.getElementById("internet").value,
        activities: document.getElementById("activities").value,
        absences: Number(document.getElementById("absences").value),
        grade_1: Number(document.getElementById("grade_1").value),
        grade_2: Number(document.getElementById("grade_2").value),
        final_grade: Number(document.getElementById("final_grade").value)
    };

    try {

       let url = "http://127.0.0.1:8000/students";
let method = "POST";

if (editingStudentId !== null) {
    url = `http://127.0.0.1:8000/students/${editingStudentId}`;
    method = "PUT";
}

const response = await fetch(url, {
    method: method,

    headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    },

    body: JSON.stringify(student)
});
if (response.status === 401) {
    localStorage.removeItem("token");
    window.location.href = "index.html";
    return;
}


        if (response.ok) {

    if (editingStudentId !== null) {

        document.getElementById("studentMessage").textContent =
            "Student updated successfully!";

    } else {

        document.getElementById("studentMessage").textContent =
            "Student added successfully!";

    }

    document.getElementById("studentForm").reset();

    editingStudentId = null;

    document.getElementById("formTitle").textContent = "Add Student";
    document.getElementById("submitStudentBtn").textContent = "Add Student";

    getStudents();

} else {
    const data = await response.json();

            document.getElementById("studentMessage").textContent =
                data.detail;

        }

    } catch (error) {

        console.error(error);

        document.getElementById("studentMessage").textContent =
            "Unable to connect to server.";

    }

});
async function deleteStudent(id) {

    const confirmDelete = confirm(
        `Are you sure you want to delete student ${id}?`
    );

    if (!confirmDelete) {
        return;
    }

    try {

        const response = await fetch(
            `http://127.0.0.1:8000/students/${id}`,
            {
                method: "DELETE",

                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );
                if (response.status === 401) {
            localStorage.removeItem("token");
            window.location.href = "index.html";
            return;
        }

        if (response.ok) {

            alert("Student deleted successfully!");

            getStudents();

        } else {

            const data = await response.json();

            alert(data.detail);

        }

    } catch (error) {

        console.error(error);

        alert("Unable to connect to server.");

    }
}
function editStudent(id) {

    const student = allStudents.find(student => student.id === id);

    if (!student) {
        return;
    }

    editingStudentId = id;

    document.getElementById("formTitle").textContent = "Edit Student";
    document.getElementById("submitStudentBtn").textContent = "Update Student";

    document.getElementById("school").value = student.school;
    document.getElementById("gender").value = student.gender;
    document.getElementById("age").value = student.age;
    document.getElementById("address").value = student.address;
    document.getElementById("study_time").value = student.study_time;
    document.getElementById("failures").value = student.failures;
    document.getElementById("internet").value = student.internet;
    document.getElementById("activities").value = student.activities;
    document.getElementById("absences").value = student.absences;
    document.getElementById("grade_1").value = student.grade_1;
    document.getElementById("grade_2").value = student.grade_2;
    document.getElementById("final_grade").value = student.final_grade;

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}