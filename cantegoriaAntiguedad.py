import os

os.system("clear")

print("Verificacion de Antiguedad")
antiguedad = int(input("Antiguedad: "))
if(antiguedad < 4):
    print("Categoria 1 - 69.68")
elif(antiguedad >= 5 and antiguedad <= 8):
    print("Categoria 2 - 74.26")
elif(antiguedad >= 9 and antiguedad <= 12):
    print("Categoria 3 - 79.98")