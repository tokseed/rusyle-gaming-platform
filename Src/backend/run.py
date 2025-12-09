import os
from dotenv import load_dotenv
from app import create_app, db

load_dotenv()

app = create_app(os.getenv('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    return {'db': db}


@app.cli.command()
def init_db():
    db.create_all()
    print('✅ DB initialized')


@app.cli.command()
def drop_db():
    if input('Sure? (yes/no): ') == 'yes':
        db.drop_all()
        print('✅ DB dropped')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )
