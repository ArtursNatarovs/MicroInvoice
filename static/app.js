var newInvoiceButton = document.getElementById("newInvoiceButton");

var newInvoiceModal = document.getElementById("staticBackdrop");
var modalBackDrop = document.getElementById("modalBackDrop");
var prepInvoiceButton = document.getElementById("prepInvoiceButton");
var invoiceItemsModal = document.getElementById("invoiceItemsModal");
var modalItemsContainers = document.getElementById("modalItemsContainers");
var modaUserContainer = document.getElementById("modaUserContainer");
var listOfInvoices = document.getElementById("listOfInvoices");
var itemCounter = 0;


function closeModal() {
    // const modal = document.getElementById("ect-eventModal");
    newInvoiceModal.style.display = "none";
    newInvoiceModal.classList.toggle("show");
    modalBackDrop.style.display = "none";
    console.log('close modal');
}

function closeItems(){
    invoiceItemsModal.style.display = "none";
    invoiceItemsModal.classList.toggle("show");
    modalItemsContainers.innerHTML = '';
    console.log('close items modal');

}

function addNewItem(){
    itemCounter++;
    modalItemsContainers.appendChild(createInvoiceRow(itemCounter));
}

function sendInvoiceData(){
    var entities = modaUserContainer.querySelectorAll('select');
    var inputs = modalItemsContainers.querySelectorAll('input, select, textarea');
    var dataToSend ={};
    entities.forEach(function(entity) {
        dataToSend[entity.name] = entity.value;
    });
    inputs.forEach(function(input) {
        dataToSend[input.name] = input.value;
    });
    $.ajax({
        url: '/receiveInvoiceData',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(dataToSend),
        success: function(response) {
            console.log("Success:", response);
            location.reload();

        },
        error: function(xhr, status, error) {
            console.error("Error:", error);
            // Handle error (e.g., showing an error message)
            alert("Failed to send innvoice data. Please try again.");
        }
    });
    closeItems();
    closeModal();
}




newInvoiceButton.onclick = function() {
    modalBackDrop.style.display = "block";
    newInvoiceModal.style.display = "block";
    newInvoiceModal.classList.toggle("show");
  }


  prepInvoiceButton.onclick = function() {
    itemCounter++;
    modalItemsContainers.appendChild(createInvoiceRow(itemCounter));
    modalBackDrop.style.display = "block";
    invoiceItemsModal.style.display = "block";
    invoiceItemsModal.classList.toggle("show");
  }













  function createInvoiceRow(index) {
    // Create the main div with classes
    const rowDiv = document.createElement("div");
    rowDiv.classList.add("row", "input-group");

    // Create label
    const label = document.createElement("label");
    label.setAttribute("for", "");
    rowDiv.appendChild(label);

    // Create 'item' input
    const itemInput = document.createElement("input");
    itemInput.classList.add("form-control");
    itemInput.type = "text";
    itemInput.name = `item_${index}`;
    itemInput.placeholder = "Invoice item";
    rowDiv.appendChild(itemInput);

    // Create 'description' input
    const descriptionInput = document.createElement("input");
    descriptionInput.classList.add("form-control");
    descriptionInput.type = "text";
    descriptionInput.name = `description_${index}`;
    descriptionInput.placeholder = "Description";
    rowDiv.appendChild(descriptionInput);

    // Create 'value' input
    const valueInput = document.createElement("input");
    valueInput.classList.add("form-control");
    valueInput.type = "number";
    valueInput.name = `value_${index}`;
    valueInput.step = "0.01";
    valueInput.placeholder = "value";
    rowDiv.appendChild(valueInput);

    // Create 'quantity' input
    const quantityInput = document.createElement("input");
    quantityInput.classList.add("form-control");
    quantityInput.type = "number";
    quantityInput.name = `quantity_${index}`;
    quantityInput.placeholder = "quantity";
    rowDiv.appendChild(quantityInput);

    // Return the constructed rowDiv
    return rowDiv;
}
