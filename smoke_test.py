from app import create_app
from app.extensions import db
from app.models import Product, User


app = create_app()

with app.app_context():
    user = User.query.filter_by(username='admin').first()
    if not user:
        raise RuntimeError('Usuário admin não foi criado.')

client = app.test_client()

response = client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
assert response.status_code == 200, response.status_code
assert b'Dashboard' in response.data

response = client.post(
    '/products/new',
    data={
        'name': 'Produto Teste',
        'category': 'Teste',
        'unit': 'un',
        'quantity': '10',
        'quantity_min': '2',
        'description': 'Produto criado no teste automatizado',
        'location': 'A1',
        'notes': 'ok',
    },
    follow_redirects=True,
)
assert response.status_code == 200
assert b'Produto cadastrado com sucesso' in response.data

with app.app_context():
    product = Product.query.filter_by(name='Produto Teste').first()
    assert product is not None
    product_id = product.id

response = client.post(
    '/movements/new',
    data={
        'product_id': product_id,
        'direction': 'OUT',
        'quantity': '3',
        'reason': 'teste_saida',
        'note': 'teste',
    },
    follow_redirects=True,
)
assert response.status_code == 200
assert b'Movimenta' in response.data

response = client.get('/reports/export/current-stock')
assert response.status_code == 200
assert response.mimetype == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

print('SMOKE_TEST_OK')
