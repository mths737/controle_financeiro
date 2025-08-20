function showDropbox() {
    let dropbox = document.getElementById('dropbox-background')
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
            <input type="date" name="data_pagamento" required>
            <button type="submit" class="btn btn-primary btn-sm">Confirmar</button>
            <button type="button" class="btn btn-secondary btn-sm" onclick="cancelar(${id})">Cancelar</button>
    `;
}

function cancelar(id) {
  const div = document.getElementById("pagar-"+id);

  div.innerHTML =
    '<button class="btn btn-success btn-sm" onclick="pagar(' + id +')">Pagar</button>';
}