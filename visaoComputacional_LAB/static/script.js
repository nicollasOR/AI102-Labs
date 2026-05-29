// Seleção de Elementos
const fotoInput = document.getElementById('fotoInput');
const btnAnalisar = document.getElementById('btnAnalisar');
const previewImg = document.getElementById('preview');
const divResultados = document.getElementById('resultados');
const loader = document.getElementById('loader');

// Endpoint da API
const API_URL = "http://127.0.0.1:8000/analisar";

/**
 * Monitora a seleção de arquivo para exibir o preview
 */
fotoInput.addEventListener('change', function() {
    if (this.files && this.files[0]) {
        const leitor = new FileReader();
        
        leitor.onload = function(e) {
            previewImg.src = e.target.result;
            previewImg.style.display = 'block';
        };
        
        leitor.readAsDataURL(this.files[0]);
        
        // Limpa resultados anteriores ao trocar a imagem
        divResultados.innerHTML = "";
    }
});

/**
 * Função principal de análise
 */
async function enviarParaAPI() {
    if (fotoInput.files.length === 0) {
        alert("Operação negada: Nenhum arquivo selecionado.");
        return;
    }

    // Configuração da Interface
    divResultados.innerHTML = "";
    loader.style.display = "block";

    const formData = new FormData();
    formData.append("arquivo", fotoInput.files[0]);

    try {
        const resposta = await fetch(API_URL, {
            method: "POST",
            body: formData
        });
        
        const json = await resposta.json();
        loader.style.display = "none";

        renderizarResultados(json);

    } catch (erro) {
        loader.style.display = "none";
        divResultados.innerHTML = `<p style="color: #ef4444;">Erro de Conexão: O servidor FastAPI está ligado no terminal?</p>`;
        console.error("Erro na requisição:", erro);
    }
}

/**
 * Renderiza os badges de resultados na tela
 */
function renderizarResultados(json) {
    if (json.sucesso && json.dados.length > 0) {
        const htmlContent = json.dados.map(tag => `
            <div class="badge">
                ${tag.nome} <span class="conf">${tag.confianca}%</span>
            </div>
        `).join('');
        
        divResultados.innerHTML = htmlContent;
    } else if (json.sucesso && json.dados.length === 0) {
        divResultados.innerHTML = `<p class="placeholder-text">Nenhuma tag relevante encontrada.</p>`;
    } else {
        divResultados.innerHTML = `<p style="color: #ef4444;">Erro da API: ${json.erro}</p>`;
    }
}

// Evento do Botão de Análise
btnAnalisar.addEventListener('click', enviarParaAPI);