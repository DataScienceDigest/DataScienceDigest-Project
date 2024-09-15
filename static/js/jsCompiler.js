// jsCompiler.js
function runJSCode(codeId, outputId) {
    const code = document.getElementById(codeId).value;

    fetch('/run_js/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ code: code }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById(outputId).innerText = data.output;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
