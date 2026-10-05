const formulario = document.getElementById("form-assistente");
const campoTexto = document.getElementById("texto");
const campoAcao = document.getElementById("acao");
const statusMensagem = document.getElementById("status");
const resultado = document.getElementById("resultado");
const historico = document.getElementById("historico");
const botaoHistorico = document.getElementById("atualizar-historico");
const botaoProcessar = formulario.querySelector('button[type="submit"]');


async function carregarHistorico() {
    historico.textContent = "Carregando histórico...";

    try {
        const resposta = await fetch("/historico");

        if (!resposta.ok) {
            throw new Error("Não foi possível consultar o histórico.");
        }

        const registros = await resposta.json();

        historico.replaceChildren();

        if (registros.length === 0) {
            historico.textContent = "Nenhuma solicitação salva ainda.";
            return;
        }

        for (const registro of registros) {
            const item = document.createElement("article");
            const titulo = document.createElement("h3");
            const texto = document.createElement("p");
            const respostaSalva = document.createElement("pre");

            const data = new Date(registro.criado_em).toLocaleString("pt-BR");

            titulo.textContent = `${registro.acao} — ${data}`;
            texto.textContent = registro.texto_recebido;
            respostaSalva.textContent = registro.resultado;

            item.append(titulo, texto, respostaSalva);
            historico.append(item);
        }
    } catch (erro) {
        historico.textContent = erro.message;
    }
}


formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    botaoProcessar.disabled = true;
    statusMensagem.textContent = "Processando...";
    resultado.textContent = "";

    try {
        const resposta = await fetch("/assistente", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                texto: campoTexto.value,
                acao: campoAcao.value,
            }),
        });

        if (!resposta.ok) {
            const erroApi = await resposta.json().catch(() => null);

            let mensagem = "Não foi possível processar. Tente novamente.";

            if (resposta.status === 422) {
                mensagem = "Confira o texto e a ação. O texto deve ter de 10 a 10.000 caracteres.";
            } else if (typeof erroApi?.detail === "string") {
                mensagem = erroApi.detail;
            }

            throw new Error(mensagem);
        }

        const dados = await resposta.json();

        resultado.textContent = dados.resultado;
        statusMensagem.textContent = "Solicitação processada e salva.";

        await carregarHistorico();
    } catch (erro) {
        statusMensagem.textContent = erro instanceof TypeError
            ? "Não foi possível conectar ao servidor. Confira se ele está ligado e tente novamente."
            : erro.message;
    } finally {
        botaoProcessar.disabled = false;
    }
});


botaoHistorico.addEventListener("click", carregarHistorico);

carregarHistorico();
