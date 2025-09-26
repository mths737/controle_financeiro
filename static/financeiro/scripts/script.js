function showDropbox() {
    let dropbox = document.getElementById('dropbox-background')
    dropbox.className = "visible"
    if(dropbox) {
        dropbox.style.display = "block"
    }
}

function select(id) {
    let lines = document.getElementsByTagName('tr');
    let id_reg = document.getElementById("id-reg");
    let form_acao = document.getElementById("form-acao");

    for (let line of lines) {
        if (line.id == id) {
            if (line.classList.contains("selected")) {
                line.classList.remove("selected");
                id_reg.value = "";
                form_acao.classList.remove("show");
            } else {
                for (let l of lines) l.classList.remove("selected");
                line.classList.add("selected");
                id_reg.value = id;
                form_acao.classList.add("show");
            }
        } else {
            line.classList.remove("selected");
        }
    }
}

function pagar(id) {
    const div = document.getElementById("pagar-"+id);
    div.style = "animation-name: form; animation-time: 1s;"

    div.innerHTML = `
    <div class="pagar">
        <div style="width: 100%; height: 50%;">
            <input onclick="event.stopPropagation()" type="date" name="data_pagamento" required>
        </div>
        <div style="display: flex; width: 50%; height: 50%; justify-content: center; align-items: center;">
            <button onclick="event.stopPropagation()" style="margin: 2px;" type="submit" class="btn btn-success">
                <i class="bi bi-check-lg"></i>
            </button>
            <button style="margin: 2px;" type="button" class="btn btn-secondary"
                onclick="handleCancelarClick(event, '${id}')">
                <i class="bi bi-x-lg"></i>
            </button>
        </div>
    </div>
`;
}

function handlePagarClick(event, id) {
    event.stopPropagation(); // não deixa o clique subir pro <tr>
    
    let row = document.getElementById(id);
    
    // se ainda não estiver selecionada, seleciona a linha
    if (!row.classList.contains("selected")) {
        select(id); 
    }

    // chama sua função pagar normalmente
    pagar(id);
}

function handleCancelarClick(event, id) {
    event.stopPropagation(); // evita desmarcar linha
    
    let div = document.getElementById("pagar-" + id);

    // volta para o botão original
    div.innerHTML = `
        <button style="padding: 0.2rem;" class="btn btn-primary btn-sm"
            onclick="handlePagarClick(event, '${id}')">
            Pagar
        </button>
    `;
}

window.addEventListener('DOMContentLoaded', function () {
    // Por ID padrão do Django: id_<nome_do_campo>
    var cpfInput = document.getElementById('id_cpf_cnpj');
    var telInput = document.getElementById('id_telefone');

    if (cpfInput) {
      Inputmask({
        mask: ["999.999.999-99", "99.999.999/9999-99"],
        keepStatic: true
      }).mask(cpfInput);
    }

    if (telInput) {
      Inputmask({
        mask: ["(99) 9999-9999", "(99) 9 9999-9999"],
        keepStatic: true
      }).mask(telInput);
    }
});

document.addEventListener('DOMContentLoaded', () => {
  const offcanvasEl = document.getElementById('filtrosOffcanvas');
  const backdrop = document.getElementById('custom-offcanvas-backdrop');

  if (!offcanvasEl || !backdrop || typeof bootstrap === 'undefined') return;

  // Obter a instância do Offcanvas
  const bsOffcanvas = bootstrap.Offcanvas.getOrCreateInstance(offcanvasEl);

  // Quando o offcanvas vai abrir -> mostra o backdrop (entrada)
  offcanvasEl.addEventListener('show.bs.offcanvas', () => {
    // remove classe de closing caso exista
    backdrop.classList.remove('closing');

    // força reflow pra garantir transição
    void backdrop.offsetWidth;

    // marca como show (entra)
    backdrop.classList.add('show');
  });

  // Quando o offcanvas vai fechar -> anima o backdrop para saída
  offcanvasEl.addEventListener('hide.bs.offcanvas', (e) => {
    // se não houver backdrop (safety)
    if (!backdrop) return;

    // inicia a animação de saída
    backdrop.classList.remove('show');
    backdrop.classList.add('closing');

    // quando terminar a transição de opacity, limpa a classe closing
    const onTransitionEnd = (ev) => {
      if (ev.propertyName !== 'opacity') return;
      backdrop.removeEventListener('transitionend', onTransitionEnd);
      backdrop.classList.remove('closing');
      // NOTA: não removemos o elemento do DOM (ele é fixo)
    };

    backdrop.addEventListener('transitionend', onTransitionEnd);
    // não prevenimos a ação do bootstrap; apenas animamos o backdrop
  });

  // Se o offcanvas foi completamente ocultado (evento final), garantir estado limpo
  offcanvasEl.addEventListener('hidden.bs.offcanvas', () => {
    backdrop.classList.remove('show', 'closing');
  });

  // Clique no backdrop fecha o offcanvas (comportamento comum)
  backdrop.addEventListener('click', () => {
    bsOffcanvas.hide();
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('notifications-container');
  if (!container) return;

  const notifications = Array.from(container.querySelectorAll('.notification'));

  notifications.forEach(notif => {
    const DURATION = parseInt(notif.dataset.duration, 10) || 4000;

    // função genérica de esconder
    const hideNotification = () => {
      const onTransitionEnd = (ev) => {
        if (ev.propertyName === 'opacity') {
          notif.removeEventListener('transitionend', onTransitionEnd);
          if (notif.parentNode) notif.parentNode.removeChild(notif);
        }
      };

      notif.addEventListener('transitionend', onTransitionEnd);

      requestAnimationFrame(() => {
        notif.classList.remove('show');
        notif.classList.add('hide');
      });

      setTimeout(() => {
        if (notif.parentNode) notif.parentNode.removeChild(notif);
      }, 700);
    };

    // Anima a entrada
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        notif.classList.add('show');
      });
    });

    // Timer de saída automática
    setTimeout(hideNotification, DURATION);

    // Clique no botão X para fechar antes
    const closeBtn = notif.querySelector('button');
    if (closeBtn) {
      closeBtn.addEventListener('click', hideNotification);
    }
  });
});