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
    event.preventDefault();

    // Lấy giá trị từ form
    const gender = document.getElementById("gender").value;
    const age = document.getElementById("age").value;
    const income = document.getElementById("income").value;
    const loan = document.getElementById("loan").value;

    // Giả lập kết quả phân loại (thực tế sẽ dùng thuật toán để tính)
    let classification = "T"; // Đây chỉ là ví dụ, thuật toán sẽ xử lý để trả về giá trị này

    // Hiển thị kết quả
    document.getElementById("classification-result").innerText = `Khách hàng này được phân loại là: ${classification}`;
});
