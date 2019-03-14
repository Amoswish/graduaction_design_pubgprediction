from flask import Flask, render_template
from flask import Blueprint,render_template,send_file
from flask import jsonify
from flask_cors import CORS
from flask import request
from static.lib.predict_process.data_process import Data_process,Data_advice
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
@app.route('/getWinprec', methods=['POST'])
def getwinprec():
    need_predict_data = request.form
    tempa = need_predict_data.to_dict()
    df = pd.read_csv("static/res/model/predictmatchdata.csv")
    newData_process = Data_process(df)
    newData_process.preprocess(tempa)
    lgb_model = joblib.load('static/res/model/lightgbm.pkl')
    newData_process.process(lgb_model)
    winprec = newData_process.postprocess()
    # finaldata = data_process(tempa,df)
    # finaldata.preprocess()
    # # tempb = tempa['usergamedata']
    # lgb_model = joblib.load('static/res/model/lightgbm.pkl')
    # pred_test = finaldata.process(lgb_model)
    # print(type(pred_test))
    response = {
        # 'msg': 'Hello, Python !'
        'msg': str(winprec)

    }
    return jsonify(response)

@app.route('/getAdvice', methods=['POST'])
def getadvice():
    need_predict_data = request.form
    tempa = need_predict_data.to_dict()
    df = pd.read_csv("static/res/model/predictmatchdata.csv")
    newData_process = Data_process(df)
    newData_process.preprocess(tempa)
    lgb_model = joblib.load('static/res/model/lightgbm.pkl')
    newData_process.process(lgb_model)
    winprec = newData_process.postprocess()
    newDataadvice = Data_advice(df)
    advice = newDataadvice.giveadvice(lgb_model,newData_process.getinputconverge())
    # finaldata = data_process(tempa,df)
    # finaldata.preprocess()
    # # tempb = tempa['usergamedata']
    # lgb_model = joblib.load('static/res/model/lightgbm.pkl')
    # pred_test = finaldata.process(lgb_model)
    # print(type(pred_test))
    response = {
        # 'msg': 'Hello, Python !'
        'msg': str(advice)

    }
    return jsonify(response)

@app.route("/charts/<chartname>")
def hello(chartname):
    sc_map = scatter_map(chartname)
    javascript_snippet = TRANSLATOR.translate(sc_map.options)
    return render_template('charts.html',
                           host=LOCAL_HOST,
                           chart_id=sc_map.chart_id,
                           renderer=sc_map.renderer,
                           my_width="100%",
                           my_height="450",
                           custom_function=javascript_snippet.function_snippet,
                           options=javascript_snippet.option_snippet,
                           script_list=sc_map.get_js_dependencies(),
                           chart_name = chartname,
                           )


def scatter_map(chartname):
    plot_data_er = np.loadtxt(open("static/res/charts-map/charts-data/plot_data_er2.csv", "rb"), delimiter=",", skiprows=0)
    plot_data_mr = np.loadtxt(open("static/res/charts-map/charts-data/plot_data_mr2.csv", "rb"), delimiter=",",skiprows=0)
    if(chartname=='erangel'):
        chartdata = plot_data_er

    else:
        chartdata = plot_data_mr
    x_lst = [v[0] for v in chartdata]
    y_lst = [v[1] for v in chartdata]
    extra_data = [v[2] for v in chartdata]
    sc = Scatter()
    sc.add(
        "scatter",
        x_lst,
        y_lst,
        symbol_size=5,
        extra_data=extra_data,
        is_visualmap=True,
        is_yaxis_inverse = True,
        is_xaxis_show = False,
        is_yaxis_show = False,
        is_splitline_show = False,
        visual_dimension=2,
        visual_orient="horizontal",
        #     visual_type="size",
        visual_range=[1500, 2200],
        visual_text_color="#000",
    )
    sc.render()
    return sc


@app.route('/leaderboardjson', methods=['GET','POST'])
def sendjson():
    if(request.method =='GET'):
        with open('static/res/spider_save_leaderboard_data/leaderboard-fpp-1.json', 'r') as f:
            leaderboardjson = json.load(f)
            return jsonify(leaderboardjson)
    else:
        mode = request.form['mode']
        teamsize = request.form['teamsize']
        filepath = 'static/res/spider_save_leaderboard_data/leaderboard-'+mode+'-'+teamsize+'.json'
        with open(filepath, 'r') as f:
            leaderboardjson = json.load(f)
            return jsonify(leaderboardjson)

if __name__ == '__main__':
    # app.debug = True
    app.run(debug = True)
