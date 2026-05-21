num1 = float (input ("Digite sua primeira nota:  "))
num2 = float (input ("Digite sua segunda nota :   "))
num3 = float (input ("Digite a terceira nota:  "))
num4 = float (input ("Digite a quarta nota:   "))

notas = [ num1 , num2 , num3 , num4 ]
print(notas)
soma = 0
quantidade = 0

for nota in notas:
    if nota >= 0 and nota <= 10 :
        soma += nota
        quantidade += 1
    else:
        print ("Nenhuma nota válida foi digitada.")
    
else:
    media = soma / quantidade
    print("A media: ", round(media, 2))