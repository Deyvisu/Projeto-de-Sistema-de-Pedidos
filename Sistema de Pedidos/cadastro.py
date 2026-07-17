import sqlite3
import bcrypt


def cadastrar_usuario(usuario, senha_pura):
    # 1. Criptografar a senha
    # O bcrypt precisa que o texto esteja em formato de bytes (por isso o .encode())
    senha_bytes = senha_pura.encode("utf-8")
    sal = bcrypt.gensalt()  # Gera uma sequência aleatória para aumentar a segurança
    senha_hash = bcrypt.hashpw(senha_bytes, sal)

    # 2. Conectar ao banco de dados
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    # Garantir que a tabela existe
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            senha_hash BLOB NOT NULL
        )
    """
    )

    try:
        # 3. Inserir no banco de dados
        # Usamos '?' para evitar ataques de SQL Injection
        cursor.execute(
            "INSERT INTO usuarios (usuario, senha_hash) VALUES (?, ?)",
            (usuario, senha_hash),
        )
        conexao.commit()
        print(f"Usuário '{usuario}' cadastrado com sucesso!")

    except sqlite3.IntegrityError:
        # Esse erro acontece se tentarem cadastrar um usuário que já existe (UNIQUE)
        print(f"Erro: O usuário '{usuario}' já existe.")

    finally:
        conexao.close()

def verificar_usuario(usuario, senha_pura):
    # 1. Conectar ao banco de dados
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    # 2. Buscar o usuário no banco de dados
    cursor.execute(
        "SELECT senha_hash FROM usuarios WHERE usuario = ?", (usuario,)
    )
    resultado = cursor.fetchone()

    if resultado is None:
        print(f"Usuário '{usuario}' não encontrado.")
        return False

    senha_hash = resultado[0]

    # 3. Verificar a senha
    senha_bytes = senha_pura.encode("utf-8")
    if bcrypt.checkpw(senha_bytes, senha_hash):
        print(f"Usuário '{usuario}' autenticado com sucesso!")
        return True
    else:
        print("Senha incorreta.")
        return False

def listar_usuarios():
    # 1. Conectar ao banco de dados
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    # 2. Buscar todos os usuários
    cursor.execute("SELECT usuario FROM usuarios")
    usuarios = cursor.fetchall()

    if not usuarios:
        print("Nenhum usuário cadastrado.")
    else:
        print("Usuários cadastrados:")
        for usuario in usuarios:
            print(f"- {usuario[0]}")

    conexao.close()

def apagar_usuario(usuario):
    # 1. Conectar ao banco de dados
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    # 2. Deletar o usuário
    cursor.execute("DELETE FROM usuarios WHERE usuario = ?", (usuario,))
    conexao.commit()

    if cursor.rowcount > 0:
        print(f"Usuário '{usuario}' apagado com sucesso.")
    else:
        print(f"Usuário '{usuario}' não encontrado.")

    conexao.close()


def itens_disponiveis():
    return [
        "Hambúrguer Simples, valor: R$ 10,00",
        "Hambúrguer Duplo, valor: R$ 15,00",
        "Cheeseburguer, valor: R$ 12,00",
        "X-Bacon, valor: R$ 14,00",
        "X-Egg, valor: R$ 13,00",
        "Batata Frita, valor: R$ 8,00",
        "Onion Rings, valor: R$ 6,00",
        "Refrigerante Lata, valor: R$ 5,00",
        "Suco Natural, valor: R$ 7,00",
        "Água Mineral, valor: R$ 3,00",
    ]

# --- Iniciando o programa ---
while True:
    print("\nBem-vindo a Hamburgueria Burguer Shotooo!")
    print("\nPara começar seu atendimento, escolha uma opção:")
    print("1. Cadastrar usuário")
    print("2. Fazer login")
    """Para fins de desenvolvimento: print("3. Listar usuários")"""
    """Para fins de desenvolvimento: print("3. Apagar usuário")"""
    print("3. Listar itens disponíveis")
    print("4. Sair")
    opcao = input("Opção: ")

    if opcao == "1" or opcao == "Cadastrar usuário" or opcao == "usuario" or opcao == "cadastro" or opcao == "cadastrar usuario":
        novo_user = input("Digite o nome de usuário: ")
        nova_senha = input("Digite a senha: ")
        cadastrar_usuario(novo_user, nova_senha)
    elif opcao == "2" or opcao == "Fazer login" or opcao == "login" or opcao == "logar":
        user_login = input("Digite o nome de usuário para login: ")
        senha_login = input("Digite a senha para login: ")
        verificar_usuario(user_login, senha_login)
    elif opcao == "3" or opcao == "Listar itens disponíveis" or opcao == "itens" or opcao == "listar itens":
        print("\nItens disponíveis:")
        for item in itens_disponiveis():
            print(f"- {item}")
    elif opcao == "4" or opcao == "Sair":
        print("Saindo do sistema.")
        break
    else:
        print("Opção inválida. Tente novamente.")
