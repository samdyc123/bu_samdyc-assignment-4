function performSearch() {
    let query = document.getElementById("query-input").value;

    if (!query) {
        alert("Please enter a search query.");
        return;
    }

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `query=${encodeURIComponent(query)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        displayResults(data.results);
        displayGraph(data.graph);
    });
}

function displayResults(results) {
    let resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = '';

    results.forEach((result, index) => {
        let div = document.createElement('div');
        div.classList.add('result-item');
        div.innerHTML = `<strong>Document ${index + 1}:</strong> <p>${result.document}</p><p class="similarity-score">Similarity: ${result.similarity.toFixed(4)}</p>`;
        resultsDiv.appendChild(div);
    });
}

function displayGraph(graphUrl) {
    let graphImage = document.getElementById("graph-image");
    graphImage.src = 'data:image/png;base64,' + graphUrl;
}
