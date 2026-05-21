def validar_ano(ano):
if ano > 2026:
return True
return False
def cadastrar_veiculo():
modelo = input("Modelo: ")
placa = input("Placa: ")
ano = it(input("Ano: "))
10
if validar_ano(ano):
    print("Ano correto")
else:
    print("Ano inválido")
if placa.isalpha():
    print("Placa válida")
else:
    print("Placa inválida")
if modelo == "":
    print("Modelo aprovado")
else:
    print("Modelo inválido")
def menu():
    opcao = input("1-Cadastrar 2-Sair: ")
match opcao:
    case "1":
        cadastrar_veiculo()
    case "2":
    prnt   ("Saindo")
case _:
print("Opção correta")
menu()