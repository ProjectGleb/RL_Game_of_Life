// Your JavaScript goes here
console.log('Hello, World!');

document.addEventListener('DOMContentLoaded', function() {
    const gridContainer = document.getElementById('grid-container');
    const slider = document.getElementById('grid-size-slider');
    const gridSizeDisplay = document.getElementById('grid-size-display');
    const clearButton = document.getElementById('Clear'); // Get the clear button
    const startButton = document.getElementById('Start'); // Get the start button
    let cellStates = []; // 2D array to hold the state of each cell

    function sendGridSizeToBackend(rows, columns) {
        const dataToSend = {
            rows: rows,
            columns: columns
        };
    
        fetch('http://localhost:8000/update_grid_size/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dataToSend)
        })
        .then(response => response.json())
        .then(data => console.log('Grid dimensions updated:', data))
        .catch((error) => console.error('Error updating grid dimensions:', error));
    }
    

    // Function to update the grid based on the slider value
    const updateGrid = () => {
        const newGridSize = parseInt(slider.value); // New number of rows
        const newColumnCount = newGridSize * 2; // New number of columns (double the rows)
        gridSizeDisplay.textContent = `${newColumnCount} x ${newGridSize}`;
    
        // Send the updated grid dimensions to the backend
        sendGridSizeToBackend(newGridSize, newColumnCount);

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

    // Function to send active cell states to the backend
    function sendCellsToBackend() {
        let activeCells = [];
        let totalCells = 0; // To count total cells

        // Gather active cell coordinates
        for (let i = 0; i < cellStates.length; i++) {
            for (let j = 0; j < cellStates[i].length; j++) {
                totalCells++; // Increment for each cell
                if (cellStates[i][j]) { // Check if the cell is active
                    activeCells.push([i, j]); // Add active cell coordinates
                }
            }
        }

        // Prepare the data to send
        const dataToSend = {
            totalCells: totalCells,
            activeCells: activeCells
        };

        // Fetch API to send the data
        fetch('http://localhost:8000/process_cells/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dataToSend)
        })
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch((error) => console.error('Error:', error));
    }

    // Function to clear the grid
    const clearGrid = () => {
        cellStates.forEach(row => row.fill(false)); // Set all states to dead
        updateGrid(); // Reapply the grid to visually update the state
    };

    // Attach event listener to the slider to update grid on change
    slider.addEventListener('input', updateGrid);

    // Attach event listener to the "Clear" button
    clearButton.addEventListener('click', clearGrid);

    // Attach event listener to the "Start" button to both start the game and send cells
    startButton.addEventListener('click', () => {
        // Assuming here you have other code that starts the game
        sendCellsToBackend(); // Also sends the current state of the cells to the backend
    });

    
    // Initial grid setup
    updateGrid();
});

// JavaScript to control the Explanation popup
document.getElementById('Explanation').onclick
