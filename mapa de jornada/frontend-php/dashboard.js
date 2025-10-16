
document.addEventListener('DOMContentLoaded', function() {
    // URL do nosso servidor back-end Python
    const API_URL = 'http://127.0.0.1:5000';

    /**
     * Função principal que busca os dados e preenche o grid.
     */
    async function carregarMapaDeJornada() {
        try {
            // 1. BUSCAR OS DADOS DO BACK-END
            const response = await fetch(`${API_URL}/obter-historico-respostas`);
            if (!response.ok) {
                throw new Error('Não foi possível buscar o histórico do servidor.');
            }
            const historico = await response.json();
            
            if (historico.length === 0) {
                console.log("Nenhum dado encontrado para exibir.");
                return;
            }

            // 2. PROCESSAR E AGRUPAR OS DADOS
            // Em vez de agrupar por dia, vamos agrupar por SUBMISSÃO.
            // A 'data' completa (com horas, minutos, segundos) é única para cada envio.
            const respostasPorSubmissao = {};
            historico.forEach(resposta => {
                const dataCompleta = resposta.data; // Chave única para cada vez que salvou
                if (!respostasPorSubmissao[dataCompleta]) {
                    respostasPorSubmissao[dataCompleta] = {};
                }
                
                let tipoMapeado = '';
                if (resposta.tipo === 'escala_emocao') tipoMapeado = 'emocao';
                if (resposta.tipo === 'escala_desejo') tipoMapeado = 'desejo';
                if (resposta.titulo.includes('autocuidado')) tipoMapeado = 'autocuidado';
                if (resposta.titulo.includes('dificuldade')) tipoMapeado = 'dificuldade';

                if (tipoMapeado) {
                    respostasPorSubmissao[dataCompleta][tipoMapeado] = resposta.emoji;
                }
            });

            // Pega uma lista de submissões únicas. Se você respondeu 20 vezes, teremos 20 aqui.
            const submissoesUnicas = Object.keys(respostasPorSubmissao).sort();

            // 3. PREENCHER O GRID
            // A lógica agora vai funcionar corretamente com as submissões individuais
            for (let i = 1; i <= 4; i++) {
                // Pega as 7 primeiras SUBMISSÕES para a semana 1, as 7 seguintes para a semana 2, etc.
                const submissoesDaSemana = submissoesUnicas.slice((i - 1) * 7, i * 7);

                if (submissoesDaSemana.length > 0) {
                    // Pega os dados da ÚLTIMA submissão daquela semana
                    const ultimaSubmissaoDaSemana = submissoesDaSemana[submissoesDaSemana.length - 1];
                    const dadosDoDia = respostasPorSubmissao[ultimaSubmissaoDaSemana];

                    ['emocao', 'desejo', 'autocuidado', 'dificuldade'].forEach(tipo => {
                        if (dadosDoDia[tipo]) {
                            const celula = document.querySelector(`.grid-cell[data-semana="${i}"][data-tipo="${tipo}"]`);
                            if (celula) {
                                celula.innerHTML = dadosDoDia[tipo];
                            }
                        }
                    });
                }
            }

        } catch (error) {
            console.error('Erro ao carregar o Mapa de Jornada:', error);
        }
    }

    
    carregarMapaDeJornada();
});