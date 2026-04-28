import sqlite3
from datetime import datetime

def connect_db():
    conn = sqlite3.connect("budget.db")
    return conn

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS transactions')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            type TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Base de datos y tablas creadas exitosamente.")

def add_transaction(amount, category, description, transaction_type):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Obtenemos la fecha exacta de hoy automáticamente
    date_today = datetime.now().strftime("%Y-%m-%d")
    
    # Usamos signos de interrogación (?) por seguridad, para evitar inyecciones SQL
    cursor.execute('''
        INSERT INTO transactions (amount, category, description, date, type)
        VALUES (?, ?, ?, ?, ?)
    ''', (amount, category, description, date_today, transaction_type))
    
    conn.commit()
    conn.close()
    print(f"✅ Registrado: {transaction_type} de ${amount} en {category}.")

# Función para calcular el saldo total
def get_balance():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Sumamos todos los ingresos
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='ingreso'")
    ingresos = cursor.fetchone()[0] or 0.0 # El 'or 0.0' evita errores si no hay registros
    
    # Sumamos todos los gastos
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='gasto'")
    gastos = cursor.fetchone()[0] or 0.0
    
    conn.close()
    
    saldo = ingresos - gastos
    return ingresos, gastos, saldo

if __name__ == "__main__":
    # 1. Nos aseguramos de que las tablas existan
    create_tables()
    
    # 2. Simulamos algunas transacciones de prueba
    add_transaction(1500.0, "Ventas", "Venta de escritorio", "ingreso")
    add_transaction(350.0, "Materiales", "Compra de madera", "gasto")
    add_transaction(120.0, "Suscripciones", "Pago de servidor", "gasto")
    
    # 3. Calculamos y mostramos el saldo
    ingresos_totales, gastos_totales, saldo_actual = get_balance()
    
    print("\n--- RESUMEN FINANCIERO ---")
    print(f"Ingresos: ${ingresos_totales}")
    print(f"Gastos:   ${gastos_totales}")
    print(f"Saldo:    ${saldo_actual}")
    print("--------------------------")