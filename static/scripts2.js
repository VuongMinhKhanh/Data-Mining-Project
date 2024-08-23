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

document.getElementById("run-algorithm").addEventListener("click", function () {
    const minSup = document.getElementById("min-sup").value;
    const minConf = document.getElementById("min-conf").value;

    // Giả lập kết quả (code thuật toán)
    let results = `MinSup: ${minSup}%, MinConf: ${minConf}%\n\nKết quả Luật Kết Hợp sẽ được hiển thị ở đây.`;

    // Hiển thị kết quả
    // document.getElementById("results-display").textContent = results;
});

$(document).ready(function() {
    $('#upload-form').on('submit', function(e) {
        e.preventDefault(); // Prevents the default form submission

        var formData = new FormData(this);

        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                // Handle the successful response here
                var frequentItemsets = JSON.parse(response.frequent_itemsets);
                var rules = JSON.parse(response.rules);

                // Prepare HTML content
                let htmlContent = '<style>' +
                  '  .itemset, .rule { margin-bottom: auto; }' + // Reduce space between itemsets and rules
                  '  h3, p { margin: auto; line-height: auto; }' + // Tighten line height and margin for headings and paragraphs
                  '</style>';

                Object.keys(frequentItemsets.itemsets).forEach(key => {
                    let items = frequentItemsets.itemsets[key]; // Array of items
                    let support = frequentItemsets.support[key]; // Corresponding support value
                    console.log(items)
                    htmlContent += `<h2>Items: ${items.join(', ')}</h2>
                                    <p>- Support: ${support.toFixed(2)}</p>`;

                    // Find and display rules related to the current itemset
                    Object.entries(rules.antecedents).forEach(([key, value])  => {
                        let antecedents = value
                        let consequents = rules.consequents[key]
                        let conf  = rules.confidence[key]
                        let lift = rules.lift[key]
                        // antecedents.every((ant, index) => ant === items[index])
                        if (Array.isArray(antecedents) && Array.isArray(consequents) &&
                        antecedents.sort().join(',') === items.sort().join(',')) {
                            htmlContent += `
                                                <h3>Luật: Nếu 1 người mua [${antecedents.join(', ')}], họ cũng sẽ mua [${consequents.join(', ')}]</h3>
                                                <p>- Confidence: ${conf.toFixed(2)}</p>
                                                <p>- Lift: ${lift.toFixed(2)}</p>
                                            `;

                            // htmlContent += '</div>'; // Close itemset div
                        }
                    });
                });

                $('#results-display').html(htmlContent);
            },
            error: function(xhr) {
                // Handle errors here
                $('#results-display').html(``);
            }
        });
        $('html, body').animate({
            scrollTop: $('#result').offset().top
        }, 1000); // 1000 milliseconds for smooth scrolling
    });
});