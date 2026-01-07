import os
from app import create_app, db
from app.models import User, Product, Category, Order, Review
from dotenv import load_dotenv

load_dotenv()

app = create_app(os.environ.get('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Create shell context for Flask CLI"""
    return {
        'db': db,
        'User': User,
        'Product': Product,
        'Category': Category,
        'Order': Order,
        'Review': Review
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
