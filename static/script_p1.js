let updateInterval = null;
const toggleFatigueState = document.getElementById("start_AD")
const toggleRawUpdates = document.getElementById("toggleUpdates")
toggleRawUpdates.addEventListener("change", function() {
    if (this.checked) {
        // Start polling
        updateInterval = setInterval(fetchEMGData, 1000);
    } else {
        // Stop polling
        clearInterval(updateInterval);
        updateInterval = null;
    }
});

toggleFatigueState.addEventListener("change", function() {
    if (this.checked) {
        // Start polling
        updateInterval = setInterval(processEMGdata, 5000);
    } else {
        // Stop polling
        clearInterval(updateInterval);
        updateInterval = null;
    }
});

function processEMGdata(){
    // define flask route for data processing 
    fetch("/processEMG")
    .then(response => response.json())
    .then(data)
}


function fetchEMGData() {
    fetch('/get_emg_data')
        .then(response => response.json())
        .then(data => {
            const values = data.data;
            for (let i = 0; i < values.length; i++) {
                document.getElementById(`emg${i + 1}`).textContent = values[i];
            }
        })
        .catch(() => {
            // On error, set values to "---"
            for (let i = 1; i <= 8; i++) {
                document.getElementById(`emg${i}`).textContent = "---";
            }
        });
}