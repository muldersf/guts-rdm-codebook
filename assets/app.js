document.addEventListener('DOMContentLoaded', function() {
    // Fetch initial data
    fetchData();

    document.getElementById('data-type-dropdown').addEventListener('change', applyFiltersAndRenderTable);
    document.getElementById('cohort-checkboxes').addEventListener('change', applyFiltersAndRenderTable);
    document.getElementById('measure-search').addEventListener('input', applyFiltersAndRenderTable);
    
    function fetchData() {
        // Fetch data from server
        fetch('data/guts-measure-overview_cropped.json') 
            .then(response => response.json())
            .then(data => {

                fetchedData = data; // Store fetched data
                console.log("Fetched data:", fetchedData); // Log fetched data to console
                // Add all potential values to the data type dropdown
                getDropdownOptions(data);
    
                // Populate checkboxes
                fillCohortCheckboxes(data);
    
                // Render the table with filtered data
                applyFiltersAndRenderTable();
            })
            .catch(error => console.error('Error:', error));
    }

    // JavaScript code to dynamically populate cohort checkboxes
    function fillCohortCheckboxes(data) {
        const checkboxesContainer = document.getElementById('cohort-checkboxes');

        // Define cohort options
        const cohorts = [
            { id: 'all-cohorts', label: 'all cohorts', value: 'all' },
            { id: 'cohort-a', label: 'cohort a', value: 'A' },
            { id: 'cohort-b', label: 'cohort b', value: 'B' },
            { id: 'cohort-c', label: 'cohort c', value: 'C' },
            { id: 'cohort-d', label: 'cohort d', value: 'D' },
            { id: 'overlapping-cohorts', label: 'overlapping cohorts', value: 'overlapping' }
        ];

        // Clear any existing checkboxes
        checkboxesContainer.innerHTML = '';

        // Populate checkboxes
        cohorts.forEach(cohort => {
            // Create a container for the checkbox and label
            const container = document.createElement('div');
            container.classList.add('checkbox-container');

            // Create the checkbox
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = cohort.id;
            checkbox.value = cohort.value;

            // Create the label
            const label = document.createElement('label');
            label.textContent = cohort.label;
            label.setAttribute('for', cohort.id);
            label.classList.add('checkbox-label');

            // Append the checkbox and label to the container
            container.appendChild(checkbox);
            container.appendChild(label);

            // Append the container to the checkboxes container
            checkboxesContainer.appendChild(container);
        });
    }

    // Function to retrieve selected cohorts
    function getSelectedCohorts() {
        console.log("Fetched data:", fetchedData);
        const checkboxes = document.querySelectorAll('#cohort-checkboxes input[type=checkbox]');
        const selectedCohorts = [];
        checkboxes.forEach(checkbox => {
            console.log("Checkbox value:", checkbox.value);
            if (checkbox.checked) {
                selectedCohorts.push(checkbox.value);
            }
        });
        return selectedCohorts;
    }

    function getDropdownOptions(data) {
        const dropdown = document.getElementById('data-type-dropdown');
        const dataTypes = [...new Set(data.map(item => item.data_type))];
        dropdown.innerHTML = ''; // Clear existing options

        // Add 'All Data Types' option
        const allOption = document.createElement('option');
        allOption.value = 'all';
        allOption.textContent = 'all data types';
        dropdown.appendChild(allOption);

        // Add options for each data type
        dataTypes.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.textContent = type;
            dropdown.appendChild(option);
        });
    }

    function applyFiltersAndRenderTable() {
        const selectedDataType = document.getElementById('data-type-dropdown').value;
        const selectedCohorts = getSelectedCohorts(); // Retrieve selected cohorts
        const measureInput = document.getElementById('measure-search').value;

        console.log("Selected cohorts:", selectedCohorts); // Log selected cohorts to console

        let filteredData = fetchedData.slice(); // Use the fetched data
        
        // Apply data type filter
        if (selectedDataType !== 'all') {
            filteredData = filteredData.filter(item => item.data_type === selectedDataType);
        }
    
        // Apply cohort filter
        if (selectedCohorts.length > 0 && !selectedCohorts.includes('all')) {
            if(selectedCohorts.includes('overlapping')) {
                filteredData = filteredData.filter(item => item.cohort.includes(','));
            } else {
                filteredData = filteredData.filter(item => {
                    const itemCohorts = item.cohort.split(',');
                    return selectedCohorts.some(cohort => itemCohorts.includes(cohort));
                });
            }
        }

        if (measureInput !== "") {
            filteredData = filteredData.filter(item => 
                item.long_name.toLowerCase().includes(measureInput.toLowerCase()) || 
                item.short_name.toLowerCase().includes(measureInput.toLowerCase())
            );
        }
        
        // Render the table with filtered data
        renderTable(filteredData);
    }

    function renderTable(data) {
        // Clear previous table
        const tableBody = document.getElementById('table-body');
        tableBody.innerHTML = '';

        // Render new table
        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.long_name}</td>
                <td>${item.short_name}</td>
                <td>${item.data_type}</td>
                <td>${item.cohort}</td>
            `;
            tableBody.appendChild(row);
        });
    }

});
