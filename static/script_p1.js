let updateIntervalRaw = null;
let updateIntervalFatigue = null;
let updateIntervalCobot = null;

const toggleRawUpdates = document.getElementById("toggleUpdates");
const toggleFatigueState = document.getElementById("start_AD");
const toggleCobotState = document.getElementById("start_CEP");
const opState = document.getElementById("OP-State");
const cobotModeDisplay = document.getElementById("Cobot-Mode");

let currentCobotState = null;
let cobotCheckFrequency = 60000; // Start with 1 minute
let cobotTimer = null;

toggleRawUpdates.addEventListener("change", function () {
    if (this.checked) {
        updateIntervalRaw = setInterval(fetchEMGData, 1000);
    } else {
        clearInterval(updateIntervalRaw);
        updateIntervalRaw = null;
    }
});

toggleFatigueState.addEventListener("change", function () {
    if (this.checked) {
        updateIntervalFatigue = setInterval(processEMGdata, 5000); // every 5 seconds
    } else {
        clearInterval(updateIntervalFatigue);
        updateIntervalFatigue = null;
    }
});

toggleCobotState.addEventListener("change", function () {
    if (this.checked) {
        startCobotMonitor(); // start monitoring
    } else {
        stopCobotMonitor(); // stop monitoring
    }
});

// Fatigue Processing
function processEMGdata() {
    opState.textContent = "Processing...";
    opState.className = "processing";

    fetch("/processEMG")
        .then(response => response.json())
        .then(data => {
            if (data.status === "OK") {
                opState.textContent = "Normal";
                opState.className = "ok";
            } else if (data.status === "No data available") {
                opState.textContent = "No data";
                opState.className = "failed";
            } else {
                opState.textContent = "Failed";
                opState.className = "failed";
            }
        })
        .catch(() => {
            opState.textContent = "Error";
            opState.className = "failed";
        });
}

// Real-Time EMG Values
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
            for (let i = 1; i <= 6; i++) {
                document.getElementById(`emg${i}`).textContent = "---";
            }
        });
}

// Cobot Monitoring Control
function startCobotMonitor() {
    if (cobotTimer !== null) clearInterval(cobotTimer);
    updateCobotMode(); // Immediate check
    cobotTimer = setInterval(updateCobotMode, cobotCheckFrequency);
}

function stopCobotMonitor() {
    if (cobotTimer !== null) {
        clearInterval(cobotTimer);
        cobotTimer = null;
    }
}

// Cobot Mode State Update and Frequency Management
function updateCobotMode() {
    fetch('/send_robot_state')
        .then(response => response.json())
        .then(data => {
            if (!("robot_state" in data)) {
                setCobotStatus("---", false);
                return;
            }

            const newState = data.robot_state;
            setCobotStatus(newState ? "Normal" : "Fatigue", newState);

            // Only act if state has changed
            if (currentCobotState === false && newState === true) {
                // Fatigue → Normal: increase interval to 10 minutes
                cobotCheckFrequency = 10 * 60 * 1000;
                restartCobotInterval();
            } else if (currentCobotState === true && newState === false) {
                // Normal → Fatigue: reset interval to 1 minute
                cobotCheckFrequency = 60 * 1000;
                restartCobotInterval();
            }

            currentCobotState = newState;
        })
        .catch(() => {
            setCobotStatus("Error", false);
        });
}

function restartCobotInterval() {
    if (cobotTimer !== null) {
        clearInterval(cobotTimer);
        cobotTimer = setInterval(updateCobotMode, cobotCheckFrequency);
    }
}

function setCobotStatus(modeText, isNormal) {
    cobotModeDisplay.textContent = modeText;
    toggleCobotState.checked = isNormal;
    toggleCobotState.disabled = !isNormal;
}

