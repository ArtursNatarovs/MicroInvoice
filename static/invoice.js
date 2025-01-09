
function fetchAndFillSettings() {
    fetch('/get-invoiceSettings')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error fetching settings:', data.error);
                return;
            }

            // Populate the form fields with the data
            document.getElementById('pmsg').value = data.pmsg;
            document.getElementById('notice').value = data.notice;
            document.getElementById('footer').value = data.footer;
        })
        .catch(error => console.error('Error:', error));
}


    async function saveSettings() {
        try {
            const pmsg = document.getElementById('pmsg').value;
            const notice = document.getElementById('notice').value;
            const footer = document.getElementById('footer').value;

            const xmlContent = `
                <?xml version="1.0" encoding="UTF-8"?>
                <settings>
                    <invoice>
                        <pmsg>${pmsg}</pmsg>
                        <notice>${notice}</notice>
                        <footer>${footer}</footer>
                    </invoice>
                </settings>
            `;

            // Save the XML (requires a server-side script)
            const response = await fetch('/save-invoiceSettings', {
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

    // Load settings when the page is loaded
window.onload = fetchAndFillSettings;
