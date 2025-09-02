function showDropbox() {
    let dropbox = document.getElementById('dropbox-background')
    dropbox.className = "visible"
    if(dropbox) {
        dropbox.style.display = "block"
    }
}

function select(id) {
    let lines = document.getElementsByTagName('tr')
    for (line in lines) {
        if (lines[line].id == id) {
            lines[line].className = "selected"
        } else {
            lines[line].className = ""
        }
    }
}

function pagar(id) {
    const div = document.getElementById("pagar-"+id);

    div.innerHTML = `
            <div style="width: 100%;">
                <input type="date" name="data_pagamento" required>
            </div>
            <div style="display: flex; width: 100%; justify-content: center; align-items: center;">
                <button style="margin: 2px;" type="submit" class="btn btn-success btn-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-lg" viewBox="0 0 16 16">
                        <path d="M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425z"/>
                    </svg>
                </button>
                <button style="margin: 2px;" type="button" class="btn btn-secondary btn-sm" onclick="cancelar(${id})">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                        <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"/>
                    </svg>
                </button>
            </div>
    `;
}

function cancelar(id) {
  const div = document.getElementById("pagar-"+id);

  div.innerHTML =
    '<button class="btn btn-primary btn-sm" onclick="pagar(' + id +')">Pagar</button>';
}