const minutesEl = document.getElementById('minutes');
const secondsEl = document.getElementById('seconds');
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const resetBtn = document.getElementById('reset-btn');
const alertEl = document.getElementById('alert-complete');

let timer;
let totalSeconds = 25 * 60;
let isRunning = false;

function updateDisplay() {
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    minutesEl.textContent = String(minutes).padStart(2, '0');
    secondsEl.textContent = String(seconds).padStart(2, '0');
}

function startTimer() {
    if (isRunning) return;
    isRunning = true;
    alertEl.style.display = 'none'; // Hide alert on start
    startBtn.style.display = 'none';
    stopBtn.style.display = 'inline-flex';

    timer = setInterval(() => {
        if (totalSeconds <= 0) {
            clearInterval(timer);
            isRunning = false;
            alertEl.style.display = 'flex'; // Show alert on completion
            stopBtn.style.display = 'none'; // Hide stop button
            startBtn.style.display = 'inline-flex'; // Show start button
            return;
        }
        totalSeconds--;
        updateDisplay();
    }, 1000);
}

function stopTimer() {
    if (!isRunning) return;
    isRunning = false;
    clearInterval(timer);
    startBtn.style.display = 'inline-flex';
    stopBtn.style.display = 'none';
}

function resetTimer() {
    stopTimer();
    totalSeconds = 25 * 60;
    updateDisplay();
    alertEl.style.display = 'none'; // Hide alert on reset
}

startBtn.addEventListener('click', startTimer);
stopBtn.addEventListener('click', stopTimer);
resetBtn.addEventListener('click', resetTimer);

// Initial setup
updateDisplay();
