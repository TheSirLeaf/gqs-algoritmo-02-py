from datetime import date, timedelta


def adicionar_habito(dados, nome):
    habito = {
        "id": dados["proximo_id"],
        "nome": nome,
        "criado_em": date.today().isoformat(),
        "conclusoes": [],
    }
    dados["proximo_id"] += 1
    dados["habitos"].append(habito)
    return habito


def buscar_habito(dados, id_habito):
    for habito in dados["habitos"]:
        if habito["id"] == id_habito:
            return habito
    return None


def remover_habito(dados, habito):
    dados["habitos"].remove(habito)


def concluir_hoje(habito):
    hoje = date.today().isoformat()
    if hoje in habito["conclusoes"]:
        return False
    habito["conclusoes"].append(hoje)
    return True


def desfazer_hoje(habito):
    hoje = date.today().isoformat()
    if hoje not in habito["conclusoes"]:
        return False
    habito["conclusoes"].remove(hoje)
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


def semana_atual():
    hoje = date.today()
    return [hoje - timedelta(days=i) for i in range(6, -1, -1)]


def resumo_semanal(dados):
    semana = semana_atual()
    inicio_semana = semana[0]

    por_dia = []
    for dia in semana:
        ativos = 0
        feitos = 0
        for habito in dados["habitos"]:
            if date.fromisoformat(habito["criado_em"]) > dia:
                continue
            ativos += 1
            if dia.isoformat() in habito["conclusoes"]:
                feitos += 1
        por_dia.append((dia, feitos, ativos))

    por_habito = []
    for habito in dados["habitos"]:
        criado_em = date.fromisoformat(habito["criado_em"])
        primeiro = max(criado_em, inicio_semana)
        possivel = max(0, (semana[-1] - primeiro).days + 1)
        feito = 0
        for dia in semana:
            if dia >= primeiro and dia.isoformat() in habito["conclusoes"]:
                feito += 1
        por_habito.append(
            {"nome": habito["nome"], "feito": feito, "possivel": possivel}
        )

    return {
        "inicio": inicio_semana,
        "fim": semana[-1],
        "por_dia": por_dia,
        "por_habito": por_habito,
        "total_feito": sum(item["feito"] for item in por_habito),
        "total_possivel": sum(item["possivel"] for item in por_habito),
    }
