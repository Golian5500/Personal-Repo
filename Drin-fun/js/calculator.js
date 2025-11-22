const screen = document.querySelector(".screen");

function buttonPressed(value) {

    // Clear
    if (value === "C") {
        screen.textContent = "";
        return;
    }

    // Equal / evaluate
    if (value === "=") {
        try {
            screen.textContent = eval(screen.textContent);
        } catch {
            screen.textContent = "Error";
        }
        return;
    }

    // Append value to screen
    screen.textContent += value;
}

// Also connect the C button
document.querySelector(".clear").addEventListener("click", () => {
    screen.textContent = "";
});
