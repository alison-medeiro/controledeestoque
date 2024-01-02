from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

app.config['DATABASE'] = 'C:/Users/aliso/OneDrive/Documents/Atividades/CONTROLE DE ESTOQUE/database.db'  # Caminho para o banco de dados

# Função para obter conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# Criação da tabela de produtos (se não existir)
def create_table():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL
            )
        ''')
        conn.commit()

# Rota para exibir os produtos cadastrados e lidar com a exclusão
@app.route('/', methods=['GET', 'POST'])
def index():
    create_table()
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        if product_id:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
                conn.commit()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
    return render_template('index.html', products=products)

# Rota para exibir o formulário de cadastro de produtos
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    create_table()
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO products (name, quantity) VALUES (?, ?)', (name, quantity))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('add_product.html')

# Rota para deletar um produto
@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
    return redirect(url_for('index'))




# Rota para editar um produto específico
@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE products SET name = ?, quantity = ? WHERE id = ?', (name, quantity, product_id))
            conn.commit()
        return redirect(url_for('index'))
    else:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
            product = cursor.fetchone()
        return render_template('edit_product.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)