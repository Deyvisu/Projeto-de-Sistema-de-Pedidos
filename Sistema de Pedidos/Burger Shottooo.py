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
    print("Aqui estão os itens disponíveis no cardápio:")
    """while True:
        resposta = input("Deseja ver os itens disponíveis? (sim/não): ").strip().lower()
        if resposta == "sim":
            break
        elif resposta == "não":
            print("Ok, você pode ver os itens disponíveis a qualquer momento.")
            return
        else:
            print("Resposta inválida. Por favor, digite 'sim' ou 'não'.")"""
    print("\nItens disponíveis:")
    itens = [
        "1. Hambúrguer Simples, valor: R$ 10,00",
        "2. Hambúrguer Duplo, valor: R$ 15,00",
        "3. Cheeseburguer, valor: R$ 12,00",
        "4. X-Bacon, valor: R$ 14,00",
        "5. X-Egg, valor: R$ 13,00",
        "6. Batata Frita, valor: R$ 8,00",
        "7. Onion Rings, valor: R$ 6,00",
        "8. Refrigerante Lata, valor: R$ 5,00",
        "9. Suco Natural, valor: R$ 7,00",
        "10. Água Mineral, valor: R$ 3,00",
    ]
    for item in itens:
        print(f"- {item}")
        if item == "1. Hambúrguer Simples, valor: R$ 10,00":
            print("Composição: Pão, hambúrguer, alface, tomate e molho especial.")
        elif item == "2. Hambúrguer Duplo, valor: R$ 15,00":
            print("Composição: Pão, dois hambúrgueres, queijo, alface, tomate e molho especial.")
        elif item == "3. Cheeseburguer, valor: R$ 12,00":
            print("Composição: Pão, hambúrguer, queijo, alface, tomate e molho especial.")
        elif item == "4. X-Bacon, valor: R$ 14,00":
            print("Composição: Pão, hambúrguer, queijo, bacon, alface, tomate e molho especial.")
        elif item == "5. X-Egg, valor: R$ 13,00":
            print("Composição: Pão, hambúrguer, queijo, ovo, alface, tomate e molho especial.")
        elif item == "6. Batata Frita, valor: R$ 8,00":
            print("Composição: Porção de batatas fritas crocantes.")
        elif item == "7. Onion Rings, valor: R$ 6,00":
            print("Composição: Anéis de cebola empanados e fritos.")
        elif item == "8. Refrigerante Lata, valor: R$ 5,00":
            print("Composição: Lata de refrigerante gelado.")
        elif item == "9. Suco Natural, valor: R$ 7,00":
            print("Composição: Suco feito com frutas frescas.")
        elif item == "10. Água Mineral, valor: R$ 3,00":
            print("Composição: Garrafa de água mineral gelada.")
        
def fazer_pedido(com_desconto=False):
    cardapio = {
        "1": ("Hambúrguer Simples", 10.00),
        "2": ("Hambúrguer Duplo", 15.00),
        "3": ("Cheeseburguer", 12.00),
        "4": ("X-Bacon", 14.00),
        "5": ("X-Egg", 13.00),
        "6": ("Batata Frita", 8.00),
        "7": ("Onion Rings", 6.00),
        "8": ("Refrigerante Lata", 5.00),
        "9": ("Suco Natural", 7.00),
        "10": ("Água Mineral", 3.00),
    }

    print("--- CARDÁPIO ---")
    for numero, (nome, preco) in cardapio.items():
        print(f"{numero}. {nome} - R$ {preco:.2f}".replace('.', ','))
    print("----------------\n")

    carrinho = []

    deseja_pedir = input("Deseja fazer um pedido? (sim/não): ").strip().lower()
    if deseja_pedir not in ["sim", "s"]:
        print("Ok, você pode fazer um pedido a qualquer momento.")
        return

    while True:
        item_codigo = input("\nDigite o número do item que deseja pedir: ").strip()

        if item_codigo in cardapio:
            nome_item, preco_item = cardapio[item_codigo]
            carrinho.append((nome_item, preco_item))
            print(f"✅ Adicionado: {nome_item} (R$ {preco_item:.2f})".replace('.', ','))
        else:
            print("❌ Opção inválida. Tente novamente.")
            continue

        mais_algo = input("\nDeseja adicionar mais algum item? (sim/não): ").strip().lower()
        if mais_algo not in ["sim", "s"]:
            break

    # Resumo da Conta
    if carrinho:
        print("\n" + "="*30)
        print("RESUMO DO SEU PEDIDO:")
        print("="*30)
        
        subtotal = 0.0
        for nome, preco in carrinho:
            print(f"- {nome}: R$ {preco:.2f}".replace('.', ','))
            subtotal += preco

        print("-" * 30)
        
        # Aplicação do desconto se estiver logado
        if com_desconto:
            porcentagem_desconto = 0.10  # 10% de desconto
            valor_desconto = subtotal * porcentagem_desconto
            total_final = subtotal - valor_desconto
            
            print(f"Subtotal: R$ {subtotal:.2f}".replace('.', ','))
            print(f"🎁 Desconto Cliente Cadastrado (10%): -R$ {valor_desconto:.2f}".replace('.', ','))
            print(f"TOTAL A PAGAR: R$ {total_final:.2f}".replace('.', ','))
        else:
            print(f"TOTAL A PAGAR: R$ {subtotal:.2f}".replace('.', ','))
            
        print("="*30)
        print("Obrigado pelo pedido!")


# --- Iniciando o programa ---

usuario_logado = None  # Variável para armazenar o usuário logado

while True:
    print("\nBem-vindo ao Burguer Shotooo!")
    if usuario_logado:
        print(f"Usuário logado, 10% de desconto disponível! Bem-vindo!")
    else:
        print("Você não está logado. Faça login para aproveitar descontos e benefícios.")

    print("\nPara começar seu atendimento, escolha uma opção:")
    print("1. Cadastrar usuário")
    print("2. Fazer login")
    """Para fins de desenvolvimento: print("3. Listar usuários")"""
    """Para fins de desenvolvimento: print("3. Apagar usuário")"""
    print("3. Listar itens disponíveis")
    print("4. Fazer pedido")
    print("5. Sair")
    opcao = input("Opção: ")

    if opcao == "1" or opcao == "Cadastrar usuário" or opcao == "usuario" or opcao == "cadastro" or opcao == "cadastrar usuario":
        novo_user = input("Digite o nome de usuário: ")
        nova_senha = input("Digite a senha: ")
        cadastrar_usuario(novo_user, nova_senha)
    elif opcao == "2" or opcao == "Fazer login" or opcao == "login" or opcao == "logar":
        user_login = input("Digite o nome de usuário para login: ")
        senha_login = input("Digite a senha para login: ")
        usuario_logado = verificar_usuario(user_login, senha_login)
    elif opcao == "3" or opcao == "Listar itens disponíveis" or opcao == "itens" or opcao == "listar itens":
        itens_disponiveis()
    elif opcao == "4" or opcao == "Fazer pedido" or opcao == "pedido":
        fazer_pedido(com_desconto=bool(usuario_logado))
    elif opcao == "5" or opcao == "Sair" or opcao == "sair" or opcao == "exit":
        print("Saindo do sistema. Volte sempre! 🍔")
        break
    else:
        print("Opção inválida. Tente novamente.")
