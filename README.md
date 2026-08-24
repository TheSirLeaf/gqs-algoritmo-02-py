# gqs-algoritmo-02-py

## Nível 1: Criação e Código Fonte (Obrigatório)
• [ ] Desenvolvimento do Código: Crie um arquivo em Python (ex: main.py)
contendo um programa funcional feito por você (pode ser desde um
print("Hello, World!") estruturado até uma lógica simples com entrada de
dados via input()).
• [ ] Estrutura do Repositório: Suba o seu código para um repositório
público no GitHub: gqs-algoritmo-02-py
• [ ] Como executar? Documente no seu README.md o passo a passo
exato utilizando o terminal/linha de comando para executar o programa
(ex: python main.py).

## Nível 2: Documentação e Explicação do Algoritmo
• [ ] O que o código faz? Explique em linguagem natural e de forma clara
qual é o propósito principal do programa que você criou.
• [ ] Detalhamento do código:
o Explique quais foram as principais funções ou comandos
utilizados (ex: print(), input(), estruturas condicionais if/else, etc.).
• [ ] Exemplo de saída: Documente exatamente o que o console exibe
quando o seu programa é executado, ilustrando com um exemplo real
de uso.

## Nível 3: Toque Profissional (Criatividade e Markdown)
• [ ] Uso avançado de Markdown: Utilize recursos visuais para enriquecer
sua documentação, como:
o Blocos de código formatados com syntax highlighting
(````python`).
o Badges (selos) de status (ex: versão do Python, linguagem).
o Tabelas ou listas organizadas para facilitar a leitura.
• [ ] Seção "Sobre o Autor": Adicione uma breve assinatura ou seção de
créditos informando quem desenvolveu o código e a documentação.

---

# Documentação do Projeto — Organizador de Hábitos no Terminal

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/status-conclu%C3%ADdo-brightgreen)
![Licen%C3%A7a](https://img.shields.io/badge/licen%C3%A7a-MIT-yellow)
![Interface](https://img.shields.io/badge/interface-terminal-lightgrey)

Programa em **Python puro** (sem bibliotecas externas) para cadastrar hábitos,
marcar conclusões diárias, acompanhar sequências de dias cumpridos e visualizar
estatísticas semanais, com dados persistidos em JSON.

## Respostas — Nível 1: Criação e Código Fonte

### Desenvolvimento do Código

Concluído. O programa foi desenvolvido do zero e está organizado em 4 módulos:

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Ponto de entrada: menu interativo, telas e fluxo do programa |
| `habitos.py` | Regras: cadastro, conclusão diária, sequência (streak), resumo semanal |
| `armazenamento.py` | Persistência dos dados em `habitos.json` |
| `interface.py` | Estilo do console: cores ANSI, tabelas, barras de progresso e validações |

### Estrutura do Repositório

Concluído. Todo o código fonte está neste repositório público:
<https://github.com/TheSirLeaf/gqs-algoritmo-02-py>

### Como executar?

Passo a passo exato utilizando o terminal:

```bash
# 1. Verifique se o Python 3 está instalado
python --version

# 2. Clone o repositório
git clone https://github.com/TheSirLeaf/gqs-algoritmo-02-py.git

# 3. Entre na pasta do projeto
cd gqs-algoritmo-02-py

# 4. Execute o programa
python main.py
```

Não é preciso instalar nenhuma dependência. O arquivo `habitos.json` (onde os
dados ficam salvos) é criado automaticamente na primeira alteração feita pelo
menu. Para sair, utilize a opção `0` ou pressione `Ctrl+C`.

## Respostas — Nível 2: Documentação e Explicação do Algoritmo

### O que o código faz?

É um **organizador de hábitos** que roda no terminal. A pessoa cadastra hábitos
(ex.: "Estudar Python", "Beber água"), marca quais cumpriu no dia e consegue
acompanhar:

- a **sequência atual** de dias consecutivos cumpridos (streak) de cada hábito;
- as **estatísticas dos últimos 7 dias**, com gráfico de barras por dia e por
  hábito, além do percentual geral de cumprimento;
- o histórico completo fica salvo em `habitos.json`, então o progresso não se
  perde quando o programa é fechado.

Detalhe justo da lógica: se você ainda não marcou o hábito hoje, a sequência
até ontem continua valendo — ela só zera quando um dia inteiro fica em branco.

### Detalhamento do código

Principais comandos e recursos utilizados:

| Recurso | Onde é usado | Para quê |
|---|---|---|
| `input()` / `print()` | menu e todas as telas | ler opções e exibir informações |
| `if` / `elif` / `else` | despacho do menu, validações | decidir o caminho da execução |
| `while True` | laço principal e validações | repetir até receber entrada válida |
| `for` | tabelas e estatísticas | percorrer hábitos e dias da semana |
| Listas e dicionários | estrutura de cada hábito | guardar nome, datas e conclusões |
| Funções e módulos | todos os arquivos | separar responsabilidades do programa |
| `open()` + `json.load()` / `json.dump()` | `armazenamento.py` | salvar e carregar os dados |
| `date.today()` e `timedelta` | `habitos.py` | calcular hoje, ontem e a semana |
| f-strings com alinhamento (`{:<{largura}}`) | `main.py` | manter as colunas das tabelas alinhadas |
| `try` / `except` | `armazenamento.py` | arquivo ausente ou corrompido não trava o app |

Duas funções centrais da lógica (em `habitos.py`):

```python
def concluir_hoje(habito):
    hoje = date.today().isoformat()
    if hoje in habito["conclusoes"]:
        return False
    habito["conclusoes"].append(hoje)
    return True


def calcular_sequencia(habito):
    dias = set(habito["conclusoes"])
    hoje = date.today()
    dia = hoje if hoje.isoformat() in dias else hoje - timedelta(days=1)
    sequencia = 0
    while dia.isoformat() in dias:
        sequencia += 1
        dia -= timedelta(days=1)
    return sequencia
```

A conversão para `set()` torna a busca por cada dia instantânea, e o `while`
caminha um dia para trás (`timedelta(days=1)`) até encontrar o primeiro buraco
na sequência.

### Exemplo de saída

Ao executar `python main.py`, o console exibe o menu abaixo (no terminal real
as cores ANSI deixam o cabeçalho ciano e as barras de progresso verdes):

```text
╔══════════════════════════════════════════════════════════════╗
║                    ORGANIZADOR DE HÁBITOS                    ║
╚══════════════════════════════════════════════════════════════╝
                      domingo, 23/08/2026
        2 hábito(s) cadastrado(s) · 2 concluído(s) hoje
────────────────────────────────────────────────────────────────
  1 │ Listar hábitos
  2 │ Adicionar hábito
  3 │ Marcar como concluído hoje
  4 │ Desmarcar conclusão de hoje
  5 │ Remover hábito
  6 │ Ver sequência de dias
  7 │ Estatísticas semanais
  0 │ Salvar e sair
────────────────────────────────────────────────────────────────
Escolha uma opção: 7

Estatísticas dos últimos 7 dias
  SEG 17/08  ░░░░░░░░░░░░░░░░░░░░░░░░  0/0
  TER 18/08  ░░░░░░░░░░░░░░░░░░░░░░░░  0/0
  QUA 19/08  ░░░░░░░░░░░░░░░░░░░░░░░░  0/0
  QUI 20/08  ░░░░░░░░░░░░░░░░░░░░░░░░  0/0
  SEX 21/08  ░░░░░░░░░░░░░░░░░░░░░░░░  0/0
  SÁB 22/08  ░░░░░░░░░░░░░░░░░░░░░░░░  0/0
  DOM 23/08  ████████████████████████  2/2

  Desempenho geral: 2/2 (100%)

Por hábito
  Beber água      ████████████████████████  1/1
  Estudar Python  ████████████████████████  1/1
```

Listagem de hábitos (opção 1):

```text
Seus hábitos
  ID  Hábito          Hoje  Seq  Total
   1  Beber água      SIM     1      1
   2  Estudar Python  SIM     1      1
```

## Respostas — Nível 3: Toque Profissional

### Uso avançado de Markdown

Esta documentação utiliza:

- **badges** de status na abertura (versão do Python, status do projeto,
  licença e tipo de interface);
- blocos de código com syntax highlighting (`python` para trechos de código e
  `bash` para comandos de execução);
- tabelas para organizar módulos, comandos e recursos;
- listas, títulos hierárquicos e separadores para facilitar a leitura.

### Sobre o Autor

**Patrick Brito** — [@TheSirLeaf](https://github.com/TheSirLeaf)

Desenvolvedor do código e autor desta documentação. Projeto criado como
exercício de algoritmos em Python (GQS), praticando listas, dicionários,
funções, estruturas condicionais, laços, manipulação de arquivos e `datetime`.

Código distribuído sob a licença MIT — consulte o arquivo [LICENSE](LICENSE).