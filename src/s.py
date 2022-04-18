from flask import Flask, jsonify,request
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import base64

app = Flask(__name__)
CORS(app)

gas,temp,threshold = 0,0,0
df = pd.DataFrame(columns=['DateTime','Gas','Temperature'])

@app.route("/set")
def set():
    global gas,temp,threshold,df
    args = request.args
    gas = args.get("gas", default=1, type=int)
    temp = args.get("temp", default=0, type=int)
    threshold = args.get("threshold", default=0, type=int)
    ct = datetime.now()
    df = df.append({'DateTime': ct,'Gas':gas,'Temperature':temp}, ignore_index = True)
    return df.to_html()

@app.route("/get")
def get():
    def get_encoded_img(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return "data:image/png;base64," + encoded_string.decode('utf-8')

    global df
    df = df.tail(10).astype({'Gas': 'int', 'Temperature': 'int'})

    # Plot temp graph
    plt.plot(df.DateTime,df.Temperature)
    plt.axhline(y=threshold, color='r', linestyle='dashed')
    plt.xticks(rotation=90)
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.savefig('temp_plot')
    plt.clf()

    # Plot gas graph
    plt.plot(df.DateTime,df.Gas)
    plt.xticks(rotation=90)
    plt.axhline(y=0.4, color='r', linestyle='dashed')
    plt.xlabel('Time')
    plt.ylabel('Gas')
    plt.savefig('gas_plot')
    plt.clf()

    tg = get_encoded_img('temp_plot.png')
    gg = get_encoded_img('gas_plot.png')

    return jsonify({
        "gas":gas,
        "temp":temp,
        "threshold":threshold,
        "gas_graph": gg,
        'temp_graph': tg
    })

if __name__ == "__main__":
    app.run(debug=True)