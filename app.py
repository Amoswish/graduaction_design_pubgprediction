from flask import Flask
from flask import Blueprint,render_template,send_file
app = Flask(__name__)

vue = Blueprint('vue',__name__,url_prefix='/vue')
@app.route('/')
@app.route('/index')
def index():
    return render_template('vue/index.html')
@app.route('/main')
def main_html():
    # return render_template('vue/main_html/main.html')
    return send_file("templates/vue/main_html/main.html")

if __name__ == '__main__':j
    app.debug = True
    app.run()
