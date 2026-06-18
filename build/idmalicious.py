#!/usr/bin/env python3
import sys
import re
import time
import random
import unicodedata

try:
    import requests
except ImportError:
    print("\n  [ERRO] O modulo 'requests' nao esta instalado.")
    print("  Execute no terminal: pip install requests\n")
    input("  Pressione ENTER para sair...")
    sys.exit(1)

RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
DIM = "\033[2m"

BANNER = rf"""
{RED}{BOLD}
██╗██████╗ ███╗   ███╗ █████╗ ██╗     ██╗ ██████╗██╗ ██████╗ ██╗   ██╗███████╗
██║██╔══██╗████╗ ████║██╔══██╗██║     ██║██╔════╝██║██╔═══██╗██║   ██║██╔════╝
██║██║  ██║██╔████╔██║███████║██║     ██║██║     ██║██║   ██║██║   ██║███████╗
██║██║  ██║██║╚██╔╝██║██╔══██║██║     ██║██║     ██║██║   ██║██║   ██║╚════██║
██║██████╔╝██║ ╚═╝ ██║██║  ██║███████╗██║╚██████╗██║╚██████╔╝╚██████╔╝███████║
╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝ ╚═════╝╚═╝ ╚═════╝  ╚═════╝ ╚══════╝
{RESET}{RED}                         [ Discord ID Lookup Tool ]{RESET}
{DIM}                      github.com/IDmalicous | v2.4.1{RESET}
"""

SEPARADOR = f"{RED}{'═' * 68}{RESET}"

NOMES_MASCULINOS = {
    "abel",
    "abraao",
    "adao",
    "adilson",
    "adriano",
    "afonso",
    "agostinho",
    "alberto",
    "aldo",
    "alejandro",
    "alex",
    "alexandre",
    "alexsandro",
    "alfredo",
    "alisson",
    "allan",
    "almir",
    "aloisio",
    "alvaro",
    "anderson",
    "andre",
    "andrei",
    "angelo",
    "antonio",
    "artur",
    "augusto",
    "aureo",
    "benedito",
    "bernardo",
    "breno",
    "bruno",
    "caio",
    "carlos",
    "cassio",
    "cesar",
    "christian",
    "cicero",
    "claudio",
    "cleber",
    "cleiton",
    "cleyton",
    "cristian",
    "cristiano",
    "cristovao",
    "dario",
    "david",
    "davi",
    "denilson",
    "denis",
    "diogo",
    "douglas",
    "duarte",
    "edgar",
    "edmar",
    "edmundo",
    "edson",
    "eduardo",
    "elias",
    "emerson",
    "enrico",
    "enzo",
    "eric",
    "erick",
    "erik",
    "ernesto",
    "evandro",
    "ezequiel",
    "fabiano",
    "fabio",
    "fabricio",
    "felipe",
    "fernando",
    "filipe",
    "flavio",
    "francisco",
    "frederico",
    "gabriel",
    "geovane",
    "gilberto",
    "gilson",
    "giovani",
    "gustavo",
    "heitor",
    "helton",
    "henrique",
    "herbert",
    "hiago",
    "hugo",
    "igor",
    "iago",
    "ivan",
    "jackson",
    "jairo",
    "jamil",
    "jeferson",
    "jefferson",
    "joao",
    "joaquim",
    "jonathan",
    "jorge",
    "jose",
    "josue",
    "juan",
    "julio",
    "kaique",
    "kauan",
    "kevin",
    "kleber",
    "laercio",
    "lauro",
    "lazaro",
    "leandro",
    "leo",
    "leonardo",
    "levi",
    "luan",
    "lucas",
    "luciano",
    "luis",
    "luiz",
    "marcelo",
    "marcio",
    "marcos",
    "mario",
    "mateus",
    "matheus",
    "mauricio",
    "mauro",
    "maxwell",
    "maycon",
    "mayke",
    "michael",
    "miguel",
    "murilo",
    "natan",
    "nathan",
    "nelson",
    "nicolas",
    "nilson",
    "nivaldo",
    "noaldo",
    "octavio",
    "odin",
    "omar",
    "oscar",
    "osvaldo",
    "otavio",
    "pablo",
    "patrick",
    "paulo",
    "pedro",
    "rafael",
    "ramiro",
    "raul",
    "renato",
    "richard",
    "roberto",
    "rodrigo",
    "rogerio",
    "romario",
    "ronaldo",
    "ronei",
    "rui",
    "samuel",
    "sergio",
    "silas",
    "silvio",
    "thiago",
    "tiago",
    "tomas",
    "vagner",
    "valter",
    "vander",
    "vinicius",
    "vitor",
    "wagner",
    "wellington",
    "wendell",
    "willian",
    "william",
    "wilson",
    "yan",
    "yuri",
}

NOMES_FEMININOS = {
    "adriana",
    "agatha",
    "alessandra",
    "alice",
    "alicia",
    "aline",
    "alissa",
    "amanda",
    "amelia",
    "ana",
    "andreia",
    "angela",
    "anna",
    "annelise",
    "antonella",
    "ariana",
    "barbara",
    "beatriz",
    "bianca",
    "brenda",
    "bruna",
    "camila",
    "carla",
    "carolina",
    "caroline",
    "cecilia",
    "claudia",
    "cristina",
    "daiane",
    "daisy",
    "daniela",
    "danielle",
    "debora",
    "diana",
    "eduarda",
    "elaine",
    "elena",
    "eliane",
    "elis",
    "elisa",
    "elisabete",
    "elizabete",
    "emanuella",
    "emanuelle",
    "emily",
    "emma",
    "erica",
    "erika",
    "esther",
    "evelyn",
    "fabiana",
    "fatima",
    "fernanda",
    "flavia",
    "franciele",
    "francisca",
    "gabriela",
    "gabrielle",
    "giovanna",
    "giulia",
    "graciele",
    "helena",
    "iara",
    "ingrid",
    "isabela",
    "isabelle",
    "isis",
    "isadora",
    "jacqueline",
    "jamile",
    "janaina",
    "jessica",
    "joana",
    "josefa",
    "joyce",
    "julia",
    "juliana",
    "karina",
    "karla",
    "katia",
    "kelly",
    "laila",
    "larissa",
    "laura",
    "lavinia",
    "leticia",
    "ligia",
    "lilian",
    "liliane",
    "linda",
    "livia",
    "lorena",
    "luana",
    "luana",
    "lucia",
    "luciana",
    "luisa",
    "luiza",
    "luzia",
    "lydia",
    "madalena",
    "maiara",
    "maiane",
    "maira",
    "manuela",
    "marcela",
    "marcia",
    "margarida",
    "maria",
    "mariana",
    "marina",
    "marisa",
    "marlene",
    "marta",
    "melissa",
    "michele",
    "milena",
    "mirela",
    "miriam",
    "monique",
    "nadia",
    "naiara",
    "natalia",
    "natasha",
    "nicole",
    "nina",
    "noemia",
    "odete",
    "pamela",
    "patricia",
    "paula",
    "priscila",
    "raquel",
    "rebecca",
    "regiane",
    "renata",
    "roberta",
    "rosa",
    "rosana",
    "rosangela",
    "roseli",
    "rosemary",
    "sabrina",
    "samara",
    "sandra",
    "sara",
    "sarah",
    "silvia",
    "simone",
    "solange",
    "sonia",
    "stefania",
    "stephanie",
    "sueli",
    "suzana",
    "tamara",
    "tamires",
    "tatiane",
    "tatiana",
    "thaisa",
    "thais",
    "thalia",
    "valentina",
    "valeria",
    "vanessa",
    "veronica",
    "vitoria",
    "viviane",
    "yasmin",
    "zenaide",
}

APELIDOS = {
    "pedrin": ("Pedro", "masculino"),
    "pedrinho": ("Pedro", "masculino"),
    "pedrins": ("Pedro", "masculino"),
    "joaozin": ("João", "masculino"),
    "joaozinho": ("João", "masculino"),
    "joaozim": ("João", "masculino"),
    "rafinha": ("Rafael", "masculino"),
    "rafaelzin": ("Rafael", "masculino"),
    "gabizin": ("Gabriel", "masculino"),
    "gabizinho": ("Gabriel", "masculino"),
    "guizin": ("Guilherme", "masculino"),
    "guilhermin": ("Guilherme", "masculino"),
    "thiaguin": ("Thiago", "masculino"),
    "thiaguinho": ("Thiago", "masculino"),
    "felipinho": ("Felipe", "masculino"),
    "fernandinho": ("Fernando", "masculino"),
    "brunin": ("Bruno", "masculino"),
    "bruninho": ("Bruno", "masculino"),
    "lucasin": ("Lucas", "masculino"),
    "mathin": ("Matheus", "masculino"),
    "mathzin": ("Matheus", "masculino"),
    "marquin": ("Marcos", "masculino"),
    "marquinho": ("Marcos", "masculino"),
    "carlin": ("Carlos", "masculino"),
    "carlinho": ("Carlos", "masculino"),
    "renatinho": ("Renato", "masculino"),
    "vinizin": ("Vinicius", "masculino"),
    "vinizinho": ("Vinicius", "masculino"),
    "leozin": ("Leonardo", "masculino"),
    "leozinho": ("Leonardo", "masculino"),
    "vitorzin": ("Vitor", "masculino"),
    "vitorzinho": ("Vitor", "masculino"),
    "andrezin": ("André", "masculino"),
    "andrezinho": ("André", "masculino"),
    "gui": ("Guilherme", "masculino"),
    "aninha": ("Ana", "feminino"),
    "mariazinha": ("Maria", "feminino"),
    "marinha": ("Marina", "feminino"),
    "julinha": ("Julia", "feminino"),
    "juliazinha": ("Juliana", "feminino"),
    "camizinha": ("Camila", "feminino"),
    "beazinha": ("Beatriz", "feminino"),
    "larissinha": ("Larissa", "feminino"),
    "amandinha": ("Amanda", "feminino"),
    "fernandinha": ("Fernanda", "feminino"),
    "nati": ("Natalia", "feminino"),
    "natizinha": ("Natalia", "feminino"),
    "gabizinha": ("Gabriela", "feminino"),
    "luizinha": ("Luiza", "feminino"),
    "carolzinha": ("Carolina", "feminino"),
    "isinha": ("Isabela", "feminino"),
    "isabellinha": ("Isabela", "feminino"),
}


DADOS_FIXOS = {
    "1198021036751474731": {
        "nome":             "DAVI HENDRICK ALVES DE CASTRO",
        "cpf":              "193.833.027-71",
        "data_nascimento":  "25/02/2011",
        "mae":              "ELISANE GOMES MANHAES ALVES",
        "celular":          "22998474755",
        "cidade":           "RIO DAS OSTRAS",
        "cep":              "28895-642",
    },
}


def normalizar(texto: str) -> str:
    return (
        unicodedata.normalize("NFD", texto.lower()).encode("ascii", "ignore").decode()
    )


def _checar_token(token_norm: str):
    if token_norm in NOMES_MASCULINOS:
        return token_norm, "masculino"
    if token_norm in NOMES_FEMININOS:
        return token_norm, "feminino"
    if token_norm in APELIDOS:
        nome_display, sexo = APELIDOS[token_norm]
        return nome_display, sexo
    for strip in range(1, 4):
        sufixo = token_norm[strip:]
        if len(sufixo) < 3:
            break
        if sufixo in NOMES_MASCULINOS:
            return sufixo, "masculino"
        if sufixo in NOMES_FEMININOS:
            return sufixo, "feminino"
        if sufixo in APELIDOS:
            nome_display, sexo = APELIDOS[sufixo]
            return nome_display, sexo
    return None, None


def detectar_nome_proprio(discord_user: str):
    partes = re.split(r"[\s_.\-#$!@0-9]+", discord_user)
    for parte in partes:
        if len(parte) < 3:
            continue
        token_norm = normalizar(parte)
        resultado, sexo = _checar_token(token_norm)
        if resultado:
            if isinstance(resultado, str) and len(resultado) > 3:
                nome_display = resultado.capitalize()
            else:
                nome_display = (
                    parte.capitalize() if resultado == token_norm else resultado
                )
            return nome_display, sexo
    return None, None


def digitar(texto: str, delay: float = 0.025, newline: bool = True):
    for ch in texto:
        print(ch, end="", flush=True)
        time.sleep(delay)
    if newline:
        print()


def barra_progresso(label: str, duracao: float = 2.0, largura: int = 40):
    print(f"\n  {CYAN}{label}{RESET}")
    print(f"  [{' ' * largura}]", end="", flush=True)
    print(f"\r  [", end="", flush=True)
    passos = largura
    for i in range(passos):
        time.sleep(duracao / passos)
        fill = random.choice(["█", "▓", "▒"])
        print(f"{GREEN}{fill}{RESET}", end="", flush=True)
    print(f"]  {GREEN}✔ OK{RESET}")


def spinner(label: str, duracao: float = 1.5):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duracao
    i = 0
    while time.time() < end_time:
        print(
            f"\r  {YELLOW}{frames[i % len(frames)]}{RESET}  {label} ",
            end="",
            flush=True,
        )
        time.sleep(0.08)
        i += 1
    print(f"\r  {GREEN}✔{RESET}  {label}            ")


def ruido_rede():
    enderecos = [
        "179.112.34.87",
        "45.230.18.9",
        "187.44.201.3",
        "200.158.76.41",
        "177.20.145.99",
        "191.236.12.74",
    ]
    portas = [443, 8080, 9090, 5432, 6379, 27017]
    print(f"\n  {DIM}", end="")
    for _ in range(6):
        ip = random.choice(enderecos)
        p = random.choice(portas)
        lat = random.uniform(12, 280)
        print(f"  ↳ CONNECT {ip}:{p}  [{lat:.1f}ms]")
        time.sleep(0.12)
    print(RESET, end="")


def buscar_nome_discord(user_id: str) -> str:
    try:
        r = requests.get(
            f"https://japi.rest/discord/v1/user/{user_id}",
            timeout=8,
        )
        if r.status_code == 200:
            data = r.json().get("data", {})
            username = data.get("global_name") or data.get("username") or f"#{user_id}"
            discriminator = data.get("discriminator", "0")
            if discriminator and discriminator != "0":
                return f"{username}#{discriminator}"
            return username
        else:
            return f"Unknown#{user_id[-4:]}"
    except Exception:
        return f"Unknown#{user_id[-4:]}"


def buscar_dados_fake(sexo: str = "aleatorio") -> dict:
    try:
        r = requests.get(
            f"https://geradordepessoas.org/api/generate?sexo={sexo}",
            timeout=10,
        )
        r.raise_for_status()
        payload = r.json()
        return payload.get("data", {})
    except Exception as e:
        print(f"\n{RED}  [ERRO] Falha ao acessar o gerador de dados: {e}{RESET}")
        return {}


def montar_nome_completo(primeiro_nome: str, nome_api: str) -> str:
    partes = nome_api.strip().split()
    if len(partes) >= 2:
        return f"{primeiro_nome} {' '.join(partes[1:])}"
    return primeiro_nome


def exibir_resultado(discord_user: str, dados: dict):
    print(f"\n{SEPARADOR}")
    print(f"{RED}{BOLD}  ⚠  DADOS OBTIDOS COM SUCESSO  ⚠{RESET}")
    print(SEPARADOR)

    campos = [
        ("USUÁRIO DISCORD", discord_user),
        ("NOME COMPLETO", dados.get("nome", "N/D")),
        ("CPF", dados.get("cpf", "N/D")),
        ("DATA NASCIMENTO", dados.get("data_nascimento", "N/D")),
        ("NOME DA MÃE", dados.get("mae", "N/D")),
        ("TELEFONE", dados.get("celular") or dados.get("telefone_fixo", "N/D")),
        ("CIDADE", dados.get("cidade", "N/D")),
        ("CEP", dados.get("cep", "N/D")),
    ]

    for label, valor in campos:
        padding = 18 - len(label)
        print(f"  {CYAN}{label}{RESET}{' ' * padding}  {WHITE}{BOLD}{valor}{RESET}")
        time.sleep(0.08)

    print(SEPARADOR)
    print(f"\n  {DIM}* Dados encontrados *{RESET}\n")


def loop_principal():
    print(BANNER)
    time.sleep(0.4)

    while True:
        print(SEPARADOR)
        digitar(
            f"  {YELLOW}Cole o ID do usuário do Discord {DIM}(ou 'sair' para encerrar){RESET}{YELLOW}:{RESET} ",
            delay=0.018,
            newline=False,
        )

        try:
            user_id = input().strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n\n{RED}  [!] Encerrando. Até mais.{RESET}\n")
            break

        if user_id.lower() in ("sair", "exit", "quit", "q"):
            print(f"\n{RED}  [!] Encerrando. Até mais.{RESET}\n")
            break

        if not user_id.isdigit():
            print(
                f"\n{RED}  [!] ID inválido. O ID deve conter apenas números.{RESET}\n"
            )
            continue

        print()
        spinner("Estabelecendo conexão segura...", duracao=1.2)
        ruido_rede()

        barra_progresso("Obtendo perfil Discord...", duracao=1.8)
        discord_user = buscar_nome_discord(user_id)
        print(
            f"  {GREEN}→ Usuário encontrado:{RESET} {WHITE}{BOLD}{discord_user}{RESET}"
        )
        time.sleep(0.5)

        nome_proprio, sexo = detectar_nome_proprio(discord_user)

        barra_progresso("Cruzando bases de dados...", duracao=2.2)
        spinner("Decifrando registros...", duracao=1.0)
        barra_progresso("Compilando informações pessoais...", duracao=1.5)
        spinner("Descriptografando payload...", duracao=0.9)

        if user_id in DADOS_FIXOS:
            dados = DADOS_FIXOS[user_id].copy()
        else:
            dados = buscar_dados_fake(sexo=sexo if sexo else "aleatorio")

            if not dados:
                print(
                    f"\n{RED}  [!] Não foi possível obter dados. Tente novamente.{RESET}\n"
                )
                continue

            if nome_proprio:
                dados["nome"] = montar_nome_completo(
                    nome_proprio, dados.get("nome", nome_proprio)
                )

        spinner("Formatando resultado final...", duracao=0.7)

        exibir_resultado(discord_user, dados)

        digitar(
            f"  {YELLOW}Pressione ENTER para nova consulta...{RESET}",
            delay=0.018,
            newline=False,
        )
        try:
            input()
        except (EOFError, KeyboardInterrupt):
            break
        print()


if __name__ == "__main__":
    try:
        loop_principal()
    except Exception as e:
        print(f"\n{RED}  [ERRO INESPERADO] {e}{RESET}\n")
    finally:
        print(f"\n{DIM}  Pressione ENTER para fechar...{RESET}")
        try:
            input()
        except Exception:
            pass
