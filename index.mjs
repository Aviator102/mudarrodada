const { useState, useEffect } = require('react');

function Home() {
  const [rodada, setRodada] = useState(1);
  const [valor, setValor] = useState("-");
  const [novaRodada, setNovaRodada] = useState("");

  const buscarStatus = async () => {
    try {
      const res = await fetch("/api/rodada");
      const data = await res.json();
      setRodada(data.rodada);
      setValor(data.valor);
    } catch (error) {
      console.error("Erro ao buscar status da rodada:", error);
    }
  };

  useEffect(() => {
    buscarStatus();
    const interval = setInterval(buscarStatus, 5000); // Atualiza a cada 5 segundos
    return () => clearInterval(interval);
  }, []);

  const alterarRodada = async () => {
    if (!novaRodada) {
      alert("Por favor, insira um número de rodada.");
      return;
    }

    try {
      const res = await fetch("/api/rodada", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rodada: novaRodada }),
      });
      const data = await res.json();
      alert(data.mensagem);
      setNovaRodada(""); // Limpa o campo de input
      buscarStatus(); // Atualiza a rodada após alterar
    } catch (error) {
      console.error("Erro ao alterar rodada:", error);
    }
  };

  return (
    <div>
      {/* Cabeçalho */}
      <header>
        <h1>Bem-vindo ao Jogo Aviator</h1>
        <p>Monitore a rodada e o valor em tempo real.</p>
      </header>

      {/* Corpo */}
      <main>
        <section id="status">
          <h2>Status da Rodada</h2>
          <p>Rodada: {rodada}</p>
          <p>Valor: {valor}</p>
        </section>

        {/* Controle */}
        <section id="controle">
          <h3>Alterar Rodada</h3>
          <input
            type="number"
            value={novaRodada}
            onChange={(e) => setNovaRodada(e.target.value)}
            placeholder="Digite nova rodada"
          />
          <button onClick={alterarRodada}>Alterar Rodada</button>
        </section>
      </main>

      {/* Rodapé */}
      <footer>
        <p>&copy; 2024 Jogo Aviator. Todos os direitos reservados.</p>
      </footer>
    </div>
  );
}

// API Route para o Next.js
export async function getServerSideProps() {
  // Variáveis globais para armazenar o estado da rodada e valor
  let rodadaAtual = 1;
  let valorAtual = "-";

  // Função para alterar a rodada via POST
  if (typeof window === 'undefined') {
    const { method } = req;
    if (method === 'POST') {
      const { rodada } = req.body;
      if (rodada && !isNaN(rodada)) {
        rodadaAtual = parseInt(rodada);
        valorAtual = "Valor atualizado"; // Aqui você pode adicionar a lógica para o valor
      }
    }
  }

  return {
    props: {
      rodada: rodadaAtual,
      valor: valorAtual,
    },
  };
}
