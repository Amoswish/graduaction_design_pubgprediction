from flask import Flask, render_template
from flask import Blueprint,render_template,send_file
from flask import jsonify
from flask_cors import CORS
from flask import request
from static.lib.predict_process.data_process import data_process
import pandas as pd
import random
import numpy as np
from pyecharts import Scatter
from pyecharts import Scatter3D
from pyecharts_javascripthon.api import TRANSLATOR
import lightgbm
from sklearn.externals import joblib
#from pyecharts.constants import DEFAULT_HOST #这句去掉
import json
LOCAL_HOST = '../static/lib/jupyter-echarts-master/echarts'
app = Flask(__name__)
cors = CORS(app, resources={r"/getMsg": {"origins": "*"}})

vue = Blueprint('vue',__name__,url_prefix='/vue')
@app.route('/')
@app.route('/index')
def index():
    return render_template('vue/index.html')

@app.route('/main')
def main_html():
    # return render_template('vue/main_html/main.html')
    # print("sss")
    return send_file("templates/vue/main_html/main.html")

@app.route('/getMsg', methods=['POST'])
def home():
    need_predict_data = request.form
    tempa = need_predict_data.to_dict()
    df = pd.read_csv("static/res/model/predictmatchdata.csv")
    finaldata = data_process(tempa,df)
    finaldata.preprocess()
    # tempb = tempa['usergamedata']
    lgb_model = joblib.load('static/res/model/lightgbm.pkl')
    pred_test = finaldata.process(lgb_model)
    # X_test = np.array(([[5.00000000e-01, 5.00000000e+00, 3.88299988e+02, 2.00000000e+00,
    #                 3.50000000e+00, 7.00000000e+00, 3.50000000e+00, 1.50000000e+00,
    #                 2.77250000e+02, 4.80000000e+01, 4.70000000e+01, 1.00000000e+00,
    #                 2.24700000e+03, 6.50000000e+00, 6.91850000e+03, 9.16666667e-01,
    #                 8.02083333e-01, 6.91850000e+03, 0.00000000e+00, 0.00000000e+00,
    #                 8.50000000e+00, 3.54299988e+02, 1.45833333e-01, 1.50507130e-03,
    #                 1.24075103e+00, 1.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    #                 8.40425532e-01, 9.78723404e-01, 9.57446809e-01, 9.78723404e-01,
    #                 8.29787234e-01, 4.25531915e-02, 9.78723404e-01, 9.57446809e-01,
    #                 1.00000000e+00, 5.10638298e-01, 5.10638298e-01, 9.89361702e-01,
    #                 7.87234043e-01, 8.72340426e-01, 9.36170213e-01, 9.78723404e-01,
    #                 7.87234043e-01, 9.36170213e-01, 1.48936170e-01, 5.10638298e-01,
    #                 9.14893617e-01, 9.14893617e-01, 4.25531915e-02, 7.02127660e-01,
    #                 7.87234043e-01, 5.10638298e-01, 5.10638298e-01, 5.10638298e-01,
    #                 1.00000000e+00, 6.00000000e+00, 5.97500000e+02, 4.00000000e+00,
    #                 5.00000000e+00, 1.10000000e+01, 5.00000000e+00, 2.00000000e+00,
    #                 3.61899994e+02, 4.80000000e+01, 4.70000000e+01, 2.00000000e+00,
    #                 2.47700000e+03, 7.00000000e+00, 7.15100000e+03, 9.68750000e-01,
    #                 8.54166667e-01, 7.15100000e+03, 0.00000000e+00, 0.00000000e+00,
    #                 1.10000000e+01, 5.85500000e+02, 2.29166667e-01, 2.01857090e-03,
    #                 1.36775267e+00, 1.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    #                 8.61702128e-01, 9.78723404e-01, 9.78723404e-01, 9.78723404e-01,
    #                 7.87234043e-01, 4.25531915e-02, 9.57446809e-01, 9.14893617e-01,
    #                 1.00000000e+00, 5.10638298e-01, 5.10638298e-01, 9.89361702e-01,
    #                 8.29787234e-01, 7.87234043e-01, 9.36170213e-01, 9.57446809e-01,
    #                 8.29787234e-01, 9.36170213e-01, 1.48936170e-01, 5.10638298e-01,
    #                 9.04255319e-01, 9.78723404e-01, 4.25531915e-02, 6.80851064e-01,
    #                 8.29787234e-01, 5.10638298e-01, 5.10638298e-01, 5.10638298e-01,
    #                 0.00000000e+00, 4.00000000e+00, 1.79100006e+02, 0.00000000e+00,
    #                 2.00000000e+00, 3.00000000e+00, 2.00000000e+00, 1.00000000e+00,
    #                 1.92600006e+02, 4.80000000e+01, 4.70000000e+01, 0.00000000e+00,
    #                 2.01700000e+03, 6.00000000e+00, 6.68600000e+03, 8.64583333e-01,
    #                 7.50000000e-01, 6.68600000e+03, 0.00000000e+00, 0.00000000e+00,
    #                 6.00000000e+00, 1.23100006e+02, 6.25000000e-02, 9.91571695e-04,
    #                 1.11374927e+00, 1.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    #                 4.78723404e-01, 9.57446809e-01, 9.14893617e-01, 4.04255319e-01,
    #                 8.93617021e-01, 4.25531915e-02, 9.78723404e-01, 8.61702128e-01,
    #                 1.00000000e+00, 5.10638298e-01, 5.10638298e-01, 5.10638298e-01,
    #                 7.65957447e-01, 9.25531915e-01, 9.14893617e-01, 9.78723404e-01,
    #                 7.65957447e-01, 9.14893617e-01, 2.97872340e-01, 5.10638298e-01,
    #                 9.25531915e-01, 7.44680851e-01, 4.25531915e-02, 8.51063830e-01,
    #                 7.65957447e-01, 5.10638298e-01, 5.10638298e-01, 5.10638298e-01,
    #                 2.00000000e+00, 1.87500000e-01, 1.26041667e+00, 1.30895462e+02,
    #                 6.04166667e-01, 1.64583333e+00, 4.85000000e+01, 9.16666667e-01,
    #                 5.20833333e-01, 1.94913330e+01, 4.80000000e+01, 4.70000000e+01,
    #                 1.25000000e-01, 1.14776257e+03, 4.14583333e+00, 2.64861279e+03,
    #                 5.05208333e-01, 5.05208333e-01, 2.64861279e+03, 5.83333333e-01,
    #                 0.00000000e+00, 2.90625000e+00, 1.47895462e+02, 1.01041667e+00,
    #                 2.94313882e-03, 6.33772790e-01, 1.00000000e+00, 0.00000000e+00,
    #                 0.00000000e+00, 9.60000000e+01]]))
    # pred_test = lgb_model.predict(X_test, num_iteration=lgb_model.best_iteration)
    print(type(pred_test))
    response = {
        # 'msg': 'Hello, Python !'
        'msg': str(pred_test.tolist().pop())

    }
    return jsonify(response)

@app.route("/charts")
def hello():
    sc_map = scatter_map()
    javascript_snippet = TRANSLATOR.translate(sc_map.options)
    return render_template('charts.html',
                           host=LOCAL_HOST,
                           chart_id=sc_map.chart_id,
                           renderer=sc_map.renderer,
                           my_width="100%",
                           my_height="600",
                           custom_function=javascript_snippet.function_snippet,
                           options=javascript_snippet.option_snippet,
                           script_list=sc_map.get_js_dependencies(),
                           )


def scatter_map():
    plot_data_er = np.loadtxt(open("static/res/charts-map/charts-data/plot_data_er2.csv", "rb"), delimiter=",", skiprows=0)
    plot_data_mr = np.loadtxt(open("static/res/charts-map/charts-data/plot_data_mr2.csv", "rb"), delimiter=",",skiprows=0)
    x_lst = [v[0] for v in plot_data_er]
    y_lst = [v[1] for v in plot_data_er]
    extra_data = [v[2] for v in plot_data_er]
    sc = Scatter()
    sc.add(
        "scatter",
        x_lst,
        y_lst,
        extra_data=extra_data,
        is_visualmap=True,
        visual_dimension=2,
        visual_orient="horizontal",
        #     visual_type="size",
        visual_range=[500, 2500],
        visual_text_color="#000",
    )
    sc.render()
    return sc


def generate_3d_random_point():
    return [random.randint(0, 100),
            random.randint(0, 100),
            random.randint(0, 100)]

@app.route('/leaderboardjson', methods=['GET','POST'])
def sendjson():
    with open('static/res/spider_save_leaderboard_data/leaderboard-fpp-1.json', 'r') as f:
        leaderboardjson = json.load(f)
        return jsonify(leaderboardjson)

if __name__ == '__main__':
    # app.debug = True
    app.run(debug = True)
