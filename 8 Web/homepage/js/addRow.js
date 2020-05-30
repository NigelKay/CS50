function addRow()
{
    // Find the table
    let tableSelector = document.getElementById('tableId').getElementsByTagName('tbody')[0];

    let newRow = tableSelector.insertRow();

    // For each column, add a cell and assign it the corrosponding value from form
    let speciesCell = newRow.insertCell(0);
    let speciesValue = document.querySelector('#speciesField').value;
    let speciesText = document.createTextNode(speciesValue);
    speciesCell.appendChild(speciesText);

    let quantityCell = newRow.insertCell(1);
    let quantityValue = document.querySelector('#quantityField').value;
    let quantityText = document.createTextNode(quantityValue);
    quantityCell.appendChild(quantityText);


    let ageCell = newRow.insertCell(2);
    let ageValue = document.querySelector('#ageField').value;
    let ageText = document.createTextNode(ageValue);
    ageCell.appendChild(ageText);

    // Reset the form
    document.querySelector('#speciesField').value = '';
    document.querySelector('#quantityField').value = 0;
    document.querySelector('#ageField').value = '';


}