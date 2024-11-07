function showAlert() {
    alert("Button clicked!");
}

const dropArea = document.getElementById('drop-area');
dropArea.addEventListener('click', () => {document.getElementById('fileElem').click();});
dropArea.addEventListener('drop', (e) => handleFiles(e.dataTransfer.files), false);
// dropArea.addEventListener('drop', handleDrop, false);
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});
/** Prevent default behaviors for drag and drop events, which opens up pdf files in the browser */
function preventDefaults (e) {
    e.preventDefault();
    e.stopPropagation();
}
/**
 * Adds files to the dropdown menu.
 * @param {FileList|string[]} filesOrFilenames - The files (click to select) or filenames (drag & drop) to add.
 * @param {FormData} [formData=null] - The form data to append the files to.
 */
function addFiles2Dropdown(filesOrFilenames, formData = null) {
    const dropdown = document.getElementById('selectPDF');
    dropdown.innerHTML='';
    for (const file of filesOrFilenames) {
        // Check if the item is a File object (drag and drop) or a string (click to select)
        if (formData && file instanceof File) {
            formData.append('file', file);
            var option = document.createElement('option'); // add name to select
            option.value = file.name;
            option.text = file.name;
            dropdown.appendChild(option);
        } else if (typeof file === 'string') {
            var option = document.createElement('option'); // add name to select
            option.value = file;
            option.text = file;
            dropdown.appendChild(option);
        }
    }
    selectPDF();
}
/**
 * Call 'upload' to add selected file to server folder
 * @param {FileList} files - The files selected.
 */
function handleFiles(files) {
    const formData = new FormData();
    addFiles2Dropdown(files, formData)
    fetch('/upload', {method: 'POST', body: formData})
    .then(response => response.json());
}
/**Selects the PDF from the dropdown menu and displays it.*/
function selectPDF() {
    var selectedPDF = document.getElementById("selectPDF").value;
    // showPDF(selectedPDF, 1);
}
/**Remove all PDF in the server folder */
function deletePDF() {
    const formData = new FormData();
    addFiles2Dropdown([], formData)
    fetch('/delete_pdf', {method: 'POST'})
    .then(response => response.text())
    .then(() => {}); //location.reload();
}
/**Call 'copy_pdf', Uses the downloaded PDF file from the system.*/
function embedPDF() {
    fetch('/embed_pdf', {method: 'POST',
        headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
        // body: JSON.stringify({indRowBlue:rowBlue})
    })
    .then(response => response.json()) // update the dropdown menu
    .then(() => {});
}

function ask() {
    const text = document.getElementById("question").value;
    fetch('/ask', {method: 'POST',
        headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json()) // update the dropdown menu
    .then(data => {
        // Display the processed text in the HTML
        document.getElementById("result").innerText = data.ant1;
    })
}