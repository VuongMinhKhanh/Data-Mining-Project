document.getElementById("load-file").addEventListener("click", function () {
    const fileInput = document.getElementById("file-input");
    const dataDisplay = document.getElementById("data-display");

    if (fileInput.files.length === 0) {
        alert("Vui lòng tải lên tệp .txt");
        return;
    }

    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = function (e) {
        const fileContent = e.target.result;
        dataDisplay.textContent = fileContent;

        // Vẽ dữ liệu
        drawData(fileContent);
    };

    reader.readAsText(file);
});

document.querySelectorAll(".algorithm-btn").forEach(button => {
    button.addEventListener("click", function () {
        document.querySelectorAll(".algorithm-btn").forEach(btn => btn.classList.remove("selected"));
        this.classList.add("selected");

        // Hiển thị tham số tương ứng
        const algo = this.getAttribute("data-algo");
        document.querySelectorAll(".params-section").forEach(param => param.classList.add("hidden"));
        document.getElementById(`${algo}-params`).classList.remove("hidden");
    });
});

document.getElementById("step-button").addEventListener("click", function () {
    runAlgorithm(true); // Chạy từng bước
});

document.getElementById("run-button").addEventListener("click", function () {
    runAlgorithm(false); // Chạy đến khi có kết quả
});

function runAlgorithm(stepByStep) {
    const selectedAlgo = document.querySelector(".algorithm-btn.selected").getAttribute("data-algo");
    let params = {};

    if (selectedAlgo === "kmeans") {
        params.k = document.getElementById("k").value;
        params.initialCentroids = document.getElementById("initial-centroids").value.split(";").map(coord => coord.trim().split(",").map(Number));
    } else if (selectedAlgo === "dbscan") {
        params.epsilon = document.getElementById("epsilon").value;
        params.minSamples = document.getElementById("min-samples").value;
    }

    // Gửi yêu cầu phân tích và cập nhật kết quả
    const infoDisplay = document.getElementById("info-display");
    infoDisplay.textContent = `Đang chạy ${selectedAlgo} với các tham số: ${JSON.stringify(params)}`;

    if (stepByStep) {
        // Logic chạy từng bước
    } else {
        // Logic chạy đến khi có kết quả
    }
}

function drawData(fileContent) {
    const canvas = document.getElementById("data-canvas");
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const lines = fileContent.trim().split("\n");
    ctx.fillStyle = "#4A148C";

    lines.forEach(line => {
        const [x, y] = line.split(",").map(Number);
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI);
        ctx.fill();
    });
}
