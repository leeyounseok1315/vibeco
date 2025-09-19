const minutesEl = document.getElementById('minutes');
const secondsEl = document.getElementById('seconds');
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const resetBtn = document.getElementById('reset-btn');
const progressCircle = document.querySelector('.progress-ring__circle');

const radius = progressCircle.r.baseVal.value;
const circumference = 2 * Math.PI * radius;

progressCircle.style.strokeDasharray = `${circumference} ${circumference}`;
progressCircle.style.strokeDashoffset = circumference;

let timer;
let totalSeconds = 25 * 60;
const initialTotalSeconds = 25 * 60; // Store the initial time
let isRunning = false;

function setProgress(percent) {
    const offset = circumference - percent / 100 * circumference;
    progressCircle.style.strokeDashoffset = offset;
}

function updateDisplay() {
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    minutesEl.textContent = String(minutes).padStart(2, '0');
    secondsEl.textContent = String(seconds).padStart(2, '0');
}

function startTimer() {
    if (isRunning) return;
    isRunning = true;
    startBtn.style.display = 'none';
    stopBtn.style.display = 'flex'; // Use flex as it's a flex container

    timer = setInterval(() => {
        if (totalSeconds <= 0) {
            clearInterval(timer);
            isRunning = false;
            // Optional: Add a sound or visual notification for completion
            return;
        }
        totalSeconds--;
        updateDisplay();
        setProgress((totalSeconds / initialTotalSeconds) * 100);
    }, 1000);
}

function stopTimer() {
    if (!isRunning) return;
    isRunning = false;
    clearInterval(timer);
    startBtn.style.display = 'flex'; // Use flex as it's a flex container
    stopBtn.style.display = 'none';
}

function resetTimer() {
    stopTimer();
    totalSeconds = initialTotalSeconds;
    updateDisplay();
    // Reset progress bar smoothly
    progressCircle.style.transition = 'stroke-dashoffset 0s'; // No animation for the jump
    setProgress(100);
    setTimeout(() => {
        // Restore the transition for future updates
        progressCircle.style.transition = 'stroke-dashoffset 0.3s linear';
    }, 10);
}

startBtn.addEventListener('click', startTimer);
stopBtn.addEventListener('click', stopTimer);
resetBtn.addEventListener('click', resetTimer);

// Initial setup
updateDisplay();
setProgress(100);
