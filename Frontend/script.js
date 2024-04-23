// Your JavaScript goes here
console.log('Hello, World!');

// script.js
document.addEventListener('DOMContentLoaded', function() {
    const gridContainer = document.getElementById('grid-container');
    const slider = document.getElementById('grid-size-slider');
    const gridSizeDisplay = document.getElementById('grid-size-display');
    const clearButton = document.getElementById('Clear'); // Get the clear button
    let cellStates = []; // 2D array to hold the state of each cell

    // Function to update the grid based on the slider value
    const updateGrid = () => {
        const newGridSize = parseInt(slider.value); // New number of rows
        const newColumnCount = newGridSize * 2; // New number of columns (double the rows)
        gridSizeDisplay.textContent = `${newColumnCount} x ${newGridSize}`;

        // Create a new temporary state array with the new dimensions
        const newCellStates = Array.from({ length: newGridSize }, () =>
            Array.from({ length: newColumnCount }, () => false)
        );

        // Copy over existing states from the old array to the new one, ensuring we don't exceed old array bounds
        for (let i = 0; i < Math.min(newGridSize, cellStates.length); i++) {
            for (let j = 0; j < Math.min(newColumnCount, cellStates[i].length); j++) {
                newCellStates[i][j] = cellStates[i][j];
            }
        }

        // Update the global cellStates with the new resized array
        cellStates = newCellStates;

        gridContainer.innerHTML = ''; // Clear existing grid
        gridContainer.style.gridTemplateColumns = `repeat(${newColumnCount}, 1fr)`;
        gridContainer.style.gridTemplateRows = `repeat(${newGridSize}, 1fr)`;

        // Populate the grid with cells
        for (let i = 0; i < newGridSize; i++) {
            for (let j = 0; j < newColumnCount; j++) {
                const cell = document.createElement('div');
                cell.classList.add('cell');

                if (cellStates[i][j]) {
                    cell.classList.add('alive');
                }

                ((x, y) => {
                    cell.addEventListener('click', () => {
                        cell.classList.toggle('alive');
                        cellStates[x][y] = !cellStates[x][y];
                    });
                })(i, j);

                gridContainer.appendChild(cell);
            }
        }
    };

    // Function to clear the grid
    const clearGrid = () => {
        cellStates.forEach(row => row.fill(false)); // Set all states to dead
        updateGrid(); // Reapply the grid to visually update the state
    };

    // Attach event listener to the slider to update grid on change
    slider.addEventListener('input', updateGrid);

    // Attach event listener to the "Clear" button
    clearButton.addEventListener('click', clearGrid);

    // Initial grid setup
    updateGrid();
});

// JavaScript to control the Explanation popup
document.getElementById('Explanation').onclick = function() {
    document.getElementById('explanationPopup').style.display = 'block'; // This shows the popup
};

document.querySelector('.close-btn').onclick = function() {
    document.getElementById('explanationPopup').style.display = 'none'; // This hides the popup
};
