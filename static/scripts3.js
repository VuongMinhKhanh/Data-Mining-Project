document.getElementById("load-file").addEventListener("click", function () {
    const fileInput = document.getElementById("file-input");
    const dataDisplay = document.getElementById("data-display");

    if (fileInput.files.length === 0) {
        alert("Vui lòng tải lên tệp .txt");
        return;
    }

    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
        const fileContent = e.target.result;
        dataDisplay.textContent = fileContent;
    };

    reader.readAsText(file);
});

document.querySelectorAll(".algorithm-btn").forEach(button => {
    button.addEventListener("click", function () {
        document.querySelectorAll(".algorithm-btn").forEach(btn => btn.classList.remove("selected"));
        this.classList.add("selected");
    });
});

document.getElementById("input-form").addEventListener("submit", function (event) {
    event.preventDefault(); // Ngăn không cho form gửi theo cách truyền thống
    // Lấy giá trị từ các trường đầu vào
    const gender = document.getElementById("gender").value === '1' ? 1 : 0; // Giới tính
    const income = parseFloat(document.getElementById("income").value); // Thu nhập
    const loan = parseFloat(document.getElementById("loan").value); // Số tiền vay

    // Lấy độ tuổi và chuyển đổi thành one-hot encoding
    const ageGroup = parseInt(document.getElementById("age").value); // Giá trị từ 1 đến 4
    const ageOneHot = [0, 0, 0, 0]; // Mảng one-hot encoding cho 4 nhóm tuổi
    if (ageGroup >= 1 && ageGroup <= 4) {
        ageOneHot[ageGroup - 1] = 1; // Đặt giá trị tương ứng thành 1
    }
     // Tạo đối tượng gửi đi
    const userInput = {
        gender: gender, // Giới tính
        income: income, // Thu nhập
        loan: loan, // Số tiền vay
        age_group_1: ageOneHot[0], // Cột one-hot cho nhóm tuổi 1
        age_group_2: ageOneHot[1], // Cột one-hot cho nhóm tuổi 2
        age_group_3: ageOneHot[2], // Cột one-hot cho nhóm tuổi 3
        age_group_4: ageOneHot[3]  // Cột one-hot cho nhóm tuổi 4
    };

    // Gửi dữ liệu bằng fetch
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userInput) // Chuyển đổi đối tượng thành JSON
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        // Lấy tất cả các button
        const buttons = document.querySelectorAll(".algorithm-btn");
        // Kiểm tra nếu có button có class 'selected' hay không
        const selectedButton = document.querySelector(".algorithm-btn.selected");

        if (selectedButton) {
            // Nếu button có class 'selected' tồn tại
            console.log(`Button được chọn là: ${selectedButton.innerText}`);
            // Kiểm tra thuộc tính data-algo của button được chọn
            if (selectedButton.getAttribute("data-algo") === "knn") {
                document.getElementById("classification-result").innerText = data.KNN;
            } else if (selectedButton.getAttribute("data-algo") === "naive-bayes") {
                document.getElementById("classification-result").innerText = data.NaiveBayes;
            } else if (selectedButton.getAttribute("data-algo") === "decision-tree") {
                document.getElementById("classification-result").innerText = data.DecisionTree;
            }
        } else {
            // Nếu không có button nào được chọn
            console.log("Không có button nào được chọn.");
        }
    })
    .catch(error => console.error('Error:', error));
});
