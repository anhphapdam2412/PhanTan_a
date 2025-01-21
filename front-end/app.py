from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/introduce')
def introduce():
    return render_template('introduce.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/products/<int:product_id>')
def product(product_id):
    if 1 <= product_id <= 12:
        return render_template(f'product{product_id}.html')
    else:
        return "Sản phẩm không tồn tại", 404


if __name__ == '__main__':
    app.run(debug=True)
