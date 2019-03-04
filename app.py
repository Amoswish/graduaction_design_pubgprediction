from flask import Flask
from flask import Blueprint,render_template,send_file
import random
from pyecharts import Scatter3D
#from pyecharts.constants import DEFAULT_HOST #这句去掉
LOCAL_HOST = ""#加上这句
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

@app.route("/charts")
def hello():
    s3d = scatter3d()
    return render_template('charts.html',
                           myechart=s3d.render_embed(),
                           host=LOCAL_HOST,
                           script_list=s3d.get_js_dependencies())


def scatter3d():
    data = [generate_3d_random_point() for _ in range(80)]
    range_color = [
        '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
        '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
    scatter3D = Scatter3D("3D scattering plot demo", width=1200, height=600)
    scatter3D.add("", data, is_visualmap=True, visual_range_color=range_color)
    return scatter3D


def generate_3d_random_point():
    return [random.randint(0, 100),
            random.randint(0, 100),
            random.randint(0, 100)]
if __name__ == '__main__':
    # app.debug = True
    app.run(debug = True)
