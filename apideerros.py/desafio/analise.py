def menu():
    opcao = input("1-Cadastrar 2-Sair: ")
    match opcao:
            case "1":
                cadastrar_veiculo()
            case "2":
                print("Saindo")
            case _:
                print("Opção incorreta")

        

def cadastrar_veiculo():
        modelo = input("Modelo: ")
        if modelo == "":
            print("Modelo inválido")
        else:
            print("Modelo aprovado")
        placa = input("Placa: ")
        if placa.isalpha():
            print("Placa válida")
        else:
            print("Placa inválida")
        def validar_ano():
            ano = int(input("ano: "))
            if ano > 2026:
                return False
            else:
                 return True
        if validar_ano():
            print("Ano correto")
        else:
            print("Ano inválido")
        
menu()