
    const editors = {};
    let currentInputResolve = null;

    function initializeEditor(editorId) {
        if (!editors[editorId]) {
            editors[editorId] = CodeMirror.fromTextArea(document.getElementById(editorId), {
                mode: 'python',
                theme: 'material',
                lineNumbers: true,
                matchBrackets: true,
                autoCloseBrackets: true,
                indentUnit: 4,
                tabSize: 4,
            });
        }
    }

    initializeEditor('code1');
    initializeEditor('code2');

    async function runCode(editorId, outputId) {
        const editor = editors[editorId];
        let code = editor.getValue();
        
        // Detect and handle input() calls
        let inputs = [];
        let inputPattern = /input\((.*?)\)/g;
        let match;

        while ((match = inputPattern.exec(code)) !== null) {
            let userInput = await getInputFromUser(match[1] ? `Input required: ${match[1]}` : 'Enter input:');
            inputs.push(userInput || ''); // Handle cancel or empty inputs
        }

        try {
            let response = await fetch('/run/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: new URLSearchParams({ 'code': code, 'inputs[]': inputs })  // Send inputs as array
            });

            let data = await response.json();
            document.getElementById(outputId).textContent = data.output || data.error;
        } catch (error) {
            console.error('Error:', error);
            document.getElementById(outputId).textContent = 'Error executing code.';
        }
    }

    // Function to handle showing the modal for input
    function getInputFromUser(message) {
        return new Promise((resolve) => {
            document.getElementById('modalPromptMessage').textContent = message;
            document.getElementById('inputModal').style.display = 'flex';
            document.getElementById('userInput').value = '';  // Clear previous input
            currentInputResolve = resolve;  // Store the resolve function
        });
    }

    // Function to submit input from the modal
    function submitInput() {
        let input = document.getElementById('userInput').value;
        if (currentInputResolve) {
            currentInputResolve(input);
            currentInputResolve = null;
        }
        document.getElementById('inputModal').style.display = 'none';  // Hide modal after submitting
    }
