from datetime import date

import armazenamento
import habitos
from interface import (
    CINZA,
    DIAS_ABREVIADOS,
    DIAS_LONGOS,
    LARGURA,
    MAGENTA,
    NEGRITO,
    RESET,
    VERDE,
    VERMELHO,
    aviso,
    barra,
    cabecalho,
    confirmar,
    erro,
    limpar_tela,
    pausar,
    pedir_numero,
    pedir_texto,
    separador,
    sucesso,
    titulo_secao,
)

OPCOES = [
    ("1", "Listar hábitos"),
    ("2", "Adicionar hábito"),
    ("3", "Marcar como concluído hoje"),
    ("4", "Desmarcar conclusão de hoje"),
    ("5", "Remover hábito"),
    ("6", "Ver sequência de dias"),
    ("7", "Estatísticas semanais"),
    ("0", "Salvar e sair"),
]


def concluido_hoje(habito):
    return date.today().isoformat() in habito["conclusoes"]


def tela_inicial(dados):
    hoje = date.today()
    cabecalho("ORGANIZADOR DE HÁBITOS")
    rodape_data = f"{DIAS_LONGOS[hoje.weekday()]}, {hoje.strftime('%d/%m/%Y')}"
    print(CINZA + rodape_data.center(LARGURA + 2) + RESET)
    feitos = sum(1 for habito in dados["habitos"] if concluido_hoje(habito))
    resumo = f"{len(dados['habitos'])} hábito(s) cadastrado(s) · {feitos} concluído(s) hoje"
    print(CINZA + resumo.center(LARGURA + 2) + RESET)
    separador()
    for numero, descricao in OPCOES:
        print(f"  {MAGENTA}{numero}{RESET} {CINZA}│{RESET} {descricao}")
    separador()


def mostrar_habitos(dados):
    titulo_secao("Seus hábitos")
    if not dados["habitos"]:
        aviso("Nenhum hábito cadastrado. Use a opção 2 para começar.")
        return
    largura_nome = max(len(habito["nome"]) for habito in dados["habitos"])
    titulo_tabela = (
        f"  {'ID':>2}  {'Hábito':<{largura_nome}}  {'Hoje':^4}  {'Seq':>3}  {'Total':>5}"
    )
    print(CINZA + NEGRITO + titulo_tabela + RESET)
    for habito in sorted(dados["habitos"], key=lambda item: item["id"]):
        feito = concluido_hoje(habito)
        marca_txt = "SIM" if feito else "NÃO"
        cor_marca = VERDE if feito else VERMELHO
        sequencia = habitos.calcular_sequencia(habito)
        cor_seq = VERDE if sequencia > 0 else CINZA
        linha = (
            f"  {habito['id']:>2}  {habito['nome']:<{largura_nome}}  "
            + cor_marca + f"{marca_txt:^4}" + RESET + "  "
            + cor_seq + f"{sequencia:>3}" + RESET + "  "
            + f"{len(habito['conclusoes']):>5}"
        )
        print(linha)


def selecionar_habito(dados):
    if not dados["habitos"]:
        aviso("Nenhum hábito cadastrado ainda.")
        return None
    mostrar_habitos(dados)
    id_escolhido = pedir_numero("\nID do hábito: ")
    habito = habitos.buscar_habito(dados, id_escolhido)
    if habito is None:
        erro(f"Não existe hábito com o ID {id_escolhido}.")
    return habito


def acao_adicionar(dados):
    titulo_secao("Novo hábito")
    nome = pedir_texto("Nome do hábito: ")
    habitos.adicionar_habito(dados, nome)
    armazenamento.salvar_dados(dados)
    sucesso(f"Hábito '{nome}' cadastrado!")


def acao_marcar(dados):
    habito = selecionar_habito(dados)
    if habito is None:
        return
    if habitos.concluir_hoje(habito):
        armazenamento.salvar_dados(dados)
        sucesso(f"'{habito['nome']}' marcado como concluído hoje!")
    else:
        aviso(f"'{habito['nome']}' já estava concluído hoje.")


def acao_desmarcar(dados):
    habito = selecionar_habito(dados)
    if habito is None:
        return
    if habitos.desfazer_hoje(habito):
        armazenamento.salvar_dados(dados)
        sucesso(f"Conclusão de hoje removida de '{habito['nome']}'.")
    else:
        aviso(f"'{habito['nome']}' não havia sido concluído hoje.")


def acao_remover(dados):
    habito = selecionar_habito(dados)
    if habito is None:
        return
    if confirmar(f"\nRemover '{habito['nome']}' e todo o seu histórico?"):
        habitos.remover_habito(dados, habito)
        armazenamento.salvar_dados(dados)
        sucesso("Hábito removido.")
    else:
        aviso("Remoção cancelada.")


def tela_sequencias(dados):
    titulo_secao("Sequência atual de dias consecutivos")
    if not dados["habitos"]:
        aviso("Nenhum hábito cadastrado ainda.")
        return
    registros = []
    for habito in dados["habitos"]:
        registros.append((habitos.calcular_sequencia(habito), habito["nome"]))
    registros.sort(key=lambda item: item[0], reverse=True)
    maior = max(registros[0][0], 1)
    largura_nome = max(len(nome) for _, nome in registros)
    for sequencia, nome in registros:
        cor = VERDE if sequencia > 0 else CINZA
        sufixo = "dia" if sequencia == 1 else "dias"
        print(
            f"  {nome:<{largura_nome}}  {barra(sequencia, maior, 16)}  "
            + cor + f"{sequencia} {sufixo}" + RESET
        )
    print(
        f"\n{CINZA}Se hoje ainda não foi concluído, a sequência até ontem é mantida.{RESET}"
    )


def tela_estatisticas(dados):
    titulo_secao("Estatísticas dos últimos 7 dias")
    if not dados["habitos"]:
        aviso("Nenhum hábito cadastrado ainda.")
        return
    resumo = habitos.resumo_semanal(dados)
    for dia, feitos, ativos in resumo["por_dia"]:
        rotulo = f"{DIAS_ABREVIADOS[dia.weekday()]} {dia.strftime('%d/%m')}"
        print(
            f"  {CINZA}{rotulo}{RESET}  {barra(feitos, ativos, 24)}  {feitos}/{ativos}"
        )
    total = resumo["total_possivel"]
    percentual = round(100 * resumo["total_feito"] / total) if total else 0
    print(
        f"\n  {NEGRITO}Desempenho geral: "
        f"{resumo['total_feito']}/{total} ({percentual}%){RESET}"
    )

    titulo_secao("Por hábito")
    largura_nome = max(len(item["nome"]) for item in resumo["por_habito"])
    for item in resumo["por_habito"]:
        print(
            f"  {item['nome']:<{largura_nome}}  "
            f"{barra(item['feito'], item['possivel'], 24)}  "
            f"{item['feito']}/{item['possivel']}"
        )


def principal():
    dados = armazenamento.carregar_dados()
    while True:
        limpar_tela()
        tela_inicial(dados)
        opcao = pedir_texto(f"{NEGRITO}Escolha uma opção: {RESET}")
        print()
        if opcao == "1":
            mostrar_habitos(dados)
        elif opcao == "2":
            acao_adicionar(dados)
        elif opcao == "3":
            acao_marcar(dados)
        elif opcao == "4":
            acao_desmarcar(dados)
        elif opcao == "5":
            acao_remover(dados)
        elif opcao == "6":
            tela_sequencias(dados)
        elif opcao == "7":
            tela_estatisticas(dados)
        elif opcao == "0":
            armazenamento.salvar_dados(dados)
            sucesso("Progresso salvo em habitos.json. Até amanhã!")
            break
        else:
            erro(f"'{opcao}' não é uma opção válida.")
        pausar()


if __name__ == "__main__":
    try:
        principal()
    except KeyboardInterrupt:
        print()
        aviso("Programa encerrado.")
