
function fetchAndFillSettings() {
    fetch('/get-settings')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error fetching settings:', data.error);
                return;
            }

            document.getElementById('server').value = data.server;
            document.getElementById('port').value = data.port;
            document.getElementById('username').value = data.username;
            document.getElementById('password').value = data.password;
            document.getElementById('message').value = data.message;
        })
        .catch(error => console.error('Error:', error));
}


    async function saveSettings() {
        try {
            const server = document.getElementById('server').value;
            const port = document.getElementById('port').value;
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const message = document.getElementById('message').value;

            const xmlContent = `
                <?xml version="1.0" encoding="UTF-8"?>
                <settings>
                    <email>
                        <server>${server}</server>
                        <port>${port}</port>
                        <username>${username}</username>
                        <password>${password}</password>
                        <message>${message}</message>
                    </email>
                </settings>
            `;

            const response = await fetch('/save-settings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/xml'
                },
                body: xmlContent
            });

            if (response.ok) {
                alert("Settings saved successfully!");
            } else {
                alert("Failed to save settings!");
            }
        } catch (error) {
            console.error("Error saving settings:", error);
        }
    }

window.onload = fetchAndFillSettings;
