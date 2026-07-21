
"""name = input("Qual seu nome? ")
print(f"Ola, {name}!")

if name == "Deyvison":
    print("Bem vindo de volta, Deyvison!")
else:
    print(f"Prazer em te conhecer, {name}!")"""

import sqlite3

# Conectar ao banco de dados
conexao = sqlite3.connect("usuarios.db")
cursor = conexao.cursor()

while True:
    print("Bem vindo ao sistema de pedidos! Registre-se ou faça login para continuar.")
    print("1. Cadastrar usuário")
    print("2. Fazer login")
    print("3. Continuar sem cadastro (sem desconto)")
    print("4. Sair")
    opcao = input("Digite uma opção: ")
    if opcao == "1":
        usuario = input("Digite o nome de usuário: ")
        senha = input("Digite a senha: ")
        try:
            cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
            conexao.commit()
            print(f"Usuário '{usuario}' cadastrado com sucesso!")
        except sqlite3.IntegrityError:
            print(f"Erro: O usuário '{usuario}' já existe.")
    elif opcao == "2":
        usuario = input("Digite o nome de usuário: ")
        senha = input("Digite a senha: ")
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
        resultado = cursor.fetchone()
        if resultado:
            print(f"Login bem-sucedido! Bem-vindo, {usuario}!")
            break
        else:
            print("Usuário ou senha incorretos. Tente novamente.")



"""nome = input("Qual seu nome? ")
print(f"Olá, {nome}!")
print("Bem-vindo ao sistema de pedidos!")

while True:
    cliente_cadastrado = input("O cliente está cadastrado? (sim/não): ").lower()
    if cliente_cadastrado == "sim":
        print("Cliente cadastrado. Prosseguindo com o pedido.")
        break
    else:
        print("Cliente não cadastrado. Por favor, cadastre o cliente antes de prosseguir e verificar o desconto.")
        break

itensPedido = []
print("Digite os itens do pedido (digite 'sair' para finalizar):"
      )
while True:
    item = input("Item: ")
    if item == "sair":
        break
    itensPedido.append(item)

print("Itens do pedido:")
for item in itensPedido:
    print(f"- {item}")

print("Digite o valor de cada item do pedido (digite 'sair' para finalizar):")
valoresPedido = []
for item in itensPedido:
    valor = float(input(f"Valor para {item}: "))
    valoresPedido.append(valor)

print("Valores dos itens do pedido:")
for i, valor in enumerate(valoresPedido):
    print(f"- {itensPedido[i]}: R$ {valor:.2f}")

if len(itensPedido) > 0:
    total = sum(valoresPedido)
    print(f"Total do pedido: R$ {total:.2f}")
    if total > 100:
        print("O pedido é grande! verificar desconto.")
        if cliente_cadastrado == "sim":
            print("Cliente cadastrado. Aplicando desconto de 10%.")
            desconto = total * 0.1
        else:
            print("Cliente não cadastrado. Nenhum desconto aplicado.")
            desconto = 0 
        total_com_desconto = total - desconto
        print(f"Total com desconto: R$ {total_com_desconto:.2f}")
    else:
        print("O pedido é pequeno. Nenhum desconto aplicado.")
if len(itensPedido) == 0:
    print("Nenhum item foi adicionado ao pedido.")
else:
    print("Pedido finalizado com sucesso!")"""


    