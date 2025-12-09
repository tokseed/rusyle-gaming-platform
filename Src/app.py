from flask import Flask, render_template

app = Flask(__name__, 
    template_folder='../templates',  # путь к шаблонам
    static_folder='assets'           # путь к статическим файлам
)

# Или если структура стандартная:
app = Flask(__name__)

@app.route('/')
def home():
    # Передача изображений в шаблон
    return render_template('index.html', 
        logo_url='images/logo.png',
        banner_url='images/banner.jpg'
    )

if __name__ == '__main__':
    app.run(debug=True)
