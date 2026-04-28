import sys
# Importamos las funciones que creaste en el otro archivo
from database import create_tables, add_transaction, get_balance

def show_menu():
    print("\n" + "="*30)
    print(" 📊 BUDGET AUTOMATOR 📊 ")
    print("="*30)
    print("1. Registrar Ingreso")
    print("2. Registrar Gasto")
    print("3. Ver Resumen Financiero")
    print("4. Salir")
    print("="*30)

def main():
    # Asegurarnos de que la base de datos esté lista al arrancar
    create_tables()
    
    while True:
        show_menu()
        choice = input("Elige una opción (1-4): ")
        
        if choice == '1' or choice == '2':
            # Operador ternario para definir el tipo según la opción
            trans_type = "ingreso" if choice == '1' else "gasto"
            
            try:
                amount = float(input(f"Ingresa el monto del {trans_type}: $"))
                category = input("¿En qué categoría?: ")
                description = input("Descripción breve: ")
                
                add_transaction(amount, category, description, trans_type)
            except ValueError:
                print("❌ Error: Por favor ingresa un número válido para el monto.")
                
        elif choice == '3':
            ingresos, gastos, saldo = get_balance()
            print("\n--- TU ESTADO DE CUENTA ---")
            print(f"💰 Ingresos Totales: ${ingresos:.2f}")
            print(f"💸 Gastos Totales:   ${gastos:.2f}")
            print("-" * 25)
            # Cambiamos el mensaje dependiendo de si estás en números rojos o verdes
            if saldo >= 0:
                print(f"✅ Saldo Actual:     ${saldo:.2f}")
            else:
                print(f"⚠️ Saldo Actual:     ${saldo:.2f}")
            print("-" * 25)
            
        elif choice == '4':
            print("\nSaliendo de Budget Automator. ¡Hasta luego!")
            sys.exit()
            
        else:
            print("❌ Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
