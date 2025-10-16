

document.addEventListener('DOMContentLoaded', function() {
    const API_URL = 'http://127.0.0.1:5000';
    const perguntasContainer = document.getElementById('perguntas-container');
    const formulario = document.getElementById('formulario-acompanhamento');

    async function carregarFormulario() {
        try {
            const response = await fetch(`${API_URL}/obter-perguntas`);
            if (!response.ok) {
                throw new Error('Não foi possível conectar ao servidor.');
            }
            const perguntas = await response.json();
            perguntasContainer.innerHTML = '';

            perguntas.forEach(pergunta => {
                const blocoPergunta = document.createElement('div');
                blocoPergunta.className = 'pergunta-bloco';
                blocoPergunta.setAttribute('data-id-pergunta', pergunta.id);

                let conteudoPergunta = `<label class="titulo-pergunta">${pergunta.ordem}. ${pergunta.titulo}</label>`;

                if (pergunta.tipo !== 'texto_livre' && pergunta.opcoes.length > 0) {
                    conteudoPergunta += '<div class="opcoes-container">';
                    pergunta.opcoes.forEach((opcao, index) => {
                        const idUnico = `pergunta-${pergunta.id}-opcao-${index}`;
                        conteudoPergunta += `
                            <div class="opcao-item">
                                <input type="radio" id="${idUnico}" name="pergunta-${pergunta.id}" value="${opcao.texto}" required>
                                <label for="${idUnico}">
                                    <span class="emoji">${opcao.emoji}</span>
                                    <span class="texto">${opcao.texto}</span>
                                </label>
                            </div>
                        `;
                    });
                    conteudoPergunta += '</div>';
                }

                if (pergunta.tipo !== 'texto_livre') {
                     conteudoPergunta += `
                        <div class="texto-opcional">
                            <label for="texto-opcional-${pergunta.id}">Você gostaria de falar mais sobre isso?</label>
                            <input type="text" id="texto-opcional-${pergunta.id}" class="input-texto-opcional" placeholder="Escreva um pouco mais...">
                        </div>
                    `;
                } else {
                    conteudoPergunta += `
                        <div class="texto-livre-container">
                             <textarea id="texto-livre-${pergunta.id}" class="textarea-livre" placeholder="Escreva livremente abaixo..."></textarea>
                        </div>
                    `;
                }
                
                blocoPergunta.innerHTML = conteudoPergunta;
                perguntasContainer.appendChild(blocoPergunta);
            });

        } catch (error) {
            console.error('Erro ao carregar o formulário:', error);
            perguntasContainer.innerHTML = '<p style="color: red;">Não foi possível carregar as perguntas. Verifique se o servidor Python (app.py) está rodando.</p>';
        }
    }

    async function salvarRespostas(event) {
        event.preventDefault();
        const respostas = [];
        const blocosPergunta = document.querySelectorAll('.pergunta-bloco');

        blocosPergunta.forEach(bloco => {
            const idPergunta = bloco.getAttribute('data-id-pergunta');
            let respostaSelecionada = null;
            let respostaTextoLivre = null;

            const inputRadioSelecionado = bloco.querySelector('input[type="radio"]:checked');
            if (inputRadioSelecionado) {
                respostaSelecionada = inputRadioSelecionado.value;
            }

            const inputTextoOpcional = bloco.querySelector('.input-texto-opcional');
            if (inputTextoOpcional && inputTextoOpcional.value.trim() !== '') {
                respostaTextoLivre = inputTextoOpcional.value.trim();
            }

            const textareaLivre = bloco.querySelector('.textarea-livre');
            if (textareaLivre && textareaLivre.value.trim() !== '') {
                respostaTextoLivre = textareaLivre.value.trim();
                respostaSelecionada = 'N/A';
            }
            
            respostas.push({
                id_pergunta: parseInt(idPergunta),
                resposta_selecionada: respostaSelecionada,
                resposta_texto_livre: respostaTextoLivre
            });
        });

        try {
            const response = await fetch(`${API_URL}/salvar-respostas`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ respostas: respostas }),
            });

            if (!response.ok) { throw new Error('Falha ao salvar as respostas.'); }

            const resultado = await response.json();
            console.log('Sucesso:', resultado);
            alert('Suas respostas foram salvas com sucesso!');

    
            formulario.reset(); // Limpa todas as seleções e textos do formulário

        } catch (error) {
            console.error('Erro ao salvar respostas:', error);
            alert('Ocorreu um erro ao salvar suas respostas. Tente novamente.');
        }
    }

    formulario.addEventListener('submit', salvarRespostas);
    carregarFormulario();
});