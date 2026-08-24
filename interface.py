import os

os.system("")

RESET = "\033[0m"
NEGRITO = "\033[1m"
VERDE = "\033[92m"
AMARELO = "\033[93m"
VERMELHO = "\033[91m"
MAGENTA = "\033[95m"
CIANO = "\033[96m"
CINZA = "\033[90m"

LARGURA = 62

DIAS_ABREVIADOS = ["SEG", "TER", "QUA", "QUI", "SEX", "SÁB", "DOM"]
DIAS_LONGOS = [
    "segunda-feira",
    "terça-feira",
    "quarta-feira",
    "quinta-feira",
    "sexta-feira",
    "sábado",
    "domingo",
]


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def _linha_centralizada(texto):
    espacos = max(0, LARGURA - len(texto))
    esquerda = espacos // 2
    return "║" + " " * esquerda + texto + " " * (espacos - esquerda) + "║"


def cabecalho(texto):
    print(CIANO + NEGRITO, end="")
    print("╔" + "═" * LARGURA + "╗")
    print(_linha_centralizada(texto))
    print("╚" + "═" * LARGURA + "╝" + RESET)


def separador():
    print(CINZA + "─" * (LARGURA + 2) + RESET)


def titulo_secao(texto):
    print(f"\n{NEGRITO}{texto}{RESET}")


def sucesso(texto):
    print(f"{VERDE}✔ {texto}{RESET}")


def erro(texto):
    print(f"{VERMELHO}✖ {texto}{RESET}")


def aviso(texto):
    print(f"{AMARELO}• {texto}{RESET}")


def pausar():
    input(f"\n{CINZA}Pressione ENTER para continuar...{RESET}")


def barra(feito, total, largura=20):
    preenchido = 0
    if total > 0:
        preenchido = round(largura * feito / total)
    return VERDE + "█" * preenchido + CINZA + "░" * (largura - preenchido) + RESET


def pedir_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        erro("Este campo não pode ficar vazio.")


def pedir_numero(mensagem):
    while True:
        bruto = input(mensagem).strip()
        if bruto.isdigit() and int(bruto) > 0:
            return int(bruto)
        erro("Digite um número maior que zero.")


def confirmar(mensagem):
    resposta = input(f"{mensagem} (s/n) ").strip().lower()
    return resposta in ("s", "sim")
