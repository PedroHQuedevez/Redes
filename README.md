# Jogo de Adivinhação - Cliente/Servidor

## Descrição

Este projeto é um jogo de adivinhação de números implementado em Python utilizando sockets para comunicação entre servidor e clientes. Os jogadores se conectam ao servidor e tentam adivinhar um número secreto gerado aleatoriamente. Cada jogador tem sua vez para jogar, e o servidor gerencia a ordem dos turnos e as respostas aos palpites.

## Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Bibliotecas:** `socket`, `threading`, `random`

## Como Executar

### Requisitos

- Python 3 instalado.

### Instruções de Execução

1. Clone o repositório:

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_DIRETORIO>
   ```

2. Execute o servidor:

   ```bash
   python servidor_jogos.py
   ```

3. Em outro terminal, execute o cliente:

   ```bash
   python client_jogos.py
   ```

4. O jogo iniciará e os jogadores poderão se conectar ao servidor.

## Como Testar

- Execute o servidor e conecte múltiplos clientes.
- Teste diferentes palpites e observe as respostas do servidor.
- Verifique o funcionamento do timeout e da gestão de turnos.

## Funcionalidades Implementadas

- Conexão de múltiplos clientes ao servidor.
- Geração de um número secreto aleatório.
- Gerenciamento de turnos entre os jogadores.
- Mensagens de feedback sobre os palpites.
- Controle de tempo limite para cada jogada.
- Remoção de jogadores desconectados.

## Possíveis Melhorias Futuras

- Implementação de uma interface gráfica para melhor experiência do usuário.
- Suporte a configurações personalizadas (intervalo de números, tempo de espera, etc.).
- Melhor tratamento de exceções e reconexão automática.
- Registros detalhados de partidas para análise de estatísticas.

---

Este projeto foi desenvolvido como parte do **Trabalho 2**.

