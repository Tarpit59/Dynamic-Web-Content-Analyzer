let urlCount = 0;

// Add new URL dynamically and display as "URL 1", "URL 2", etc.
document.getElementById('addUrlBtn').addEventListener('click', function () {
    const newUrl = document.getElementById('newUrl').value;
    if (newUrl) {
        urlCount++;
        const urlLabel = 'URL ' + urlCount;

        const urlItem = document.createElement('div');
        urlItem.classList.add('url-item');

        const label = document.createElement('label');
        label.classList.add('url-label');
        label.innerHTML = `<strong>${urlLabel}:</strong> ${newUrl}`;

        const deleteBtn = document.createElement('button');
        deleteBtn.classList.add('deleteBtn');
        deleteBtn.textContent = 'Delete';

        urlItem.appendChild(label);
        urlItem.appendChild(deleteBtn);

        document.getElementById('urlList').appendChild(urlItem);

        document.getElementById('newUrl').value = '';

        deleteBtn.addEventListener('click', function () {
            urlItem.remove();
            updateUrlLabels();
        });
    }
});

// Update the labels of the remaining URLs after one is deleted
function updateUrlLabels() {
    const urlItems = Array.from(document.querySelectorAll('#urlList .url-item'));
    urlItems.forEach((item, index) => {
        const label = item.querySelector('.url-label');
        const urlText = label.textContent.split(': ')[1];
        label.innerHTML = `<strong>URL ${index + 1}:</strong> ${urlText}`;
    });
    urlCount = urlItems.length;
}

// Handle form submission and send URLs to Flask backend
document.getElementById('urlForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const urls = Array.from(document.querySelectorAll('#urlList .url-label')).map(item => item.textContent.split(': ')[1]);

    if (urls.length === 0) {
        alert("Please enter at least one URL");
        return;
    }

    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ urls: urls }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.invalid_urls && data.invalid_urls.length > 0) {
            let errorMessage = 'The following URLs could not be scrapped:\n';
            data.invalid_urls.forEach(urlInfo => {
                errorMessage += `- ${urlInfo.URL}:\nERROR : ${urlInfo.issue}\n`;
            });
            alert(errorMessage);
        } else {
            if (data.word_clouds) {
                displayWordClouds(data.word_clouds);
            }

            if (data.sentiment_comparison) {
                renderSentimentChart(data.sentiment_comparison);
            }

            if (data.readability_comparison) {
                renderReadabilityChart(data.readability_comparison);
            }
        }
    })
    .catch(error => {
        console.error('Error fetching analysis:', error);
        alert('An error occurred while processing the request. Please try again.');
    });
});

// Function to display word clouds in a 4x4 grid format
function displayWordClouds(wordClouds) {
    const wordCloudContainer = document.getElementById('word-cloud-container');
    wordCloudContainer.innerHTML = '';

    const title = document.createElement('h2');
    title.innerText = 'Word Cloud Chart';
    title.style = 'text-align: center; margin-bottom: 20px;';
    wordCloudContainer.appendChild(title);
    
    let row;
    wordClouds.forEach((cloudData, index) => {
        if (index % 4 === 0) {
            row = document.createElement('div');
            row.style = 'display: flex; justify-content: space-between; margin-bottom: 20px;';
            wordCloudContainer.appendChild(row);
        }

        const container = document.createElement('div');
        container.style = 'width: 23%; text-align: center; margin-right: 10px;';

        const img = document.createElement('img');
        if (cloudData.word_cloud) {
            img.src = 'data:image/png;base64,' + cloudData.word_cloud;
        } else {
            img.alt = 'Word Cloud not available';
        }
        img.alt = 'Word Cloud for ' + cloudData.URL;
        img.style = 'width: 100%;';

        container.appendChild(img);

        const label = document.createElement('p');
        label.innerText = `URL ${index + 1}`;
        container.appendChild(label);

        row.appendChild(container);
    });
}

// Function to render sentiment comparison chart
function renderSentimentChart(sentimentData) {
    const urls = sentimentData.map((_, index) => `URL ${index + 1}`);
    const positive = sentimentData.map(item => item.Positive);
    const neutral = sentimentData.map(item => item.Neutral);
    const negative = sentimentData.map(item => item.Negative);

    const avgPositive = positive.reduce((a, b) => a + b, 0) / positive.length;
    const avgNeutral = neutral.reduce((a, b) => a + b, 0) / neutral.length;
    const avgNegative = negative.reduce((a, b) => a + b, 0) / negative.length;

    const trace1 = {
        x: urls,
        y: positive,
        name: 'Positive',
        type: 'bar',
        marker: { color: '#2E4250' },
    };

    const trace2 = {
        x: urls,
        y: neutral,
        name: 'Neutral',
        type: 'bar',
        marker: { color: '#4A6A81' },
    };

    const trace3 = {
        x: urls,
        y: negative,
        name: 'Negative',
        type: 'bar',
        marker: { color: '#6D91AB' },
    };

    const avgTrace1 = {
        x: ['Average'],
        y: [avgPositive],
        name: 'Avg Positive',
        type: 'bar',
        marker: { color: '#3E3B52' },
    };

    const avgTrace2 = {
        x: ['Average'],
        y: [avgNeutral],
        name: 'Avg Neutral',
        type: 'bar',
        marker: { color: '#5E597C' },
    };

    const avgTrace3 = {
        x: ['Average'],
        y: [avgNegative],
        name: 'Avg Negative',
        type: 'bar',
        marker: { color: '#9591AF' },
    };

    const data = [trace1, trace2, trace3, avgTrace1, avgTrace2, avgTrace3];

    const layout = {
        title: '<B>Sentiment Comparison Across URLs</B>',
        barmode: 'stack',
        xaxis: { title: 'URLs' },
        yaxis: { title: 'Sentiment Score' },
        showlegend: true,
    };

    Plotly.react('sentimentChart', data, layout);
}

// Function to render readability comparison chart
function renderReadabilityChart(readabilityData) {
    const urls = readabilityData.map((_, index) => `URL ${index + 1}`);
    const readabilityScores = readabilityData.map(item => item.Readability);

    const avgReadability = readabilityScores.reduce((a, b) => a + b, 0) / readabilityScores.length;

    const trace = {
        x: urls,
        y: readabilityScores,
        type: 'bar',
        name: 'Readability Score',
        marker: { color: 'purple' },
    };

    const avgTrace = {
        x: ['Average'],
        y: [avgReadability],
        type: 'bar',
        name: 'Avg Readability',
        marker: { color: 'gray' },
    };

    const data = [trace, avgTrace];

    const layout = {
        title: '<B>Readability Score Comparison Across URLs</B>',
        xaxis: { title: 'URLs' },
        yaxis: { title: 'Readability Score' },
        showlegend: true,
    };

    Plotly.newPlot('readabilityChart', data, layout);
}

// Function to delete a URL dynamically and update the numbering
function deleteUrl(id) {
    const urlItem = document.getElementById(`urlItem-${id}`);
    if (urlItem) {
        urlItem.remove();
        urlCount--;

        const urlItems = document.querySelectorAll('.url-item');
        urlItems.forEach((item, index) => {
            const label = item.querySelector('.url-label');
            const newLabel = `URL ${index + 1}:`;
            label.textContent = newLabel + label.textContent.split(':')[1];
            item.querySelector('.deleteBtn').setAttribute('onclick', `deleteUrl(${index + 1})`);
        });
    }
}
