import matplotlib
matplotlib.use("Agg")
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, url_for, render_template,request, redirect
import io
import base64

my_stringIObytes = io.BytesIO()
app = Flask(__name__)
app.thread=False
image = ""
@app.route("/")
def home():
    return render_template("taylor_series.html",image=image)

@app.route("/results")
def results():
    my_stringIObytes.flush()
    args = request.args
    expr = sp.S(args['expr'])
    print("expr", expr)
    xco=np.arange(0,10)
    yco=np.asarray([expr.evalf(subs={x:_}) for _ in xco])
    plt.close()
    plt.plot(xco,yco)
    plt.savefig("temp.jpg")
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    with open("temp.jpg","r") as f:
        my_base64_jpgData = base64.b64encode(f.read())
        my_base64_jpgData.decode('utf-8')
    image="data:image/jpg;base64," + str(my_base64_jpgData)
    return redirect("/")

if __name__ == "__main__":
    x=sp.symbols('x')
    expr = sp.S(input("Expression please"))
    xco=np.arange(0,10)
    yco=np.asarray([expr.evalf(subs={x:_}) for _ in xco])
    plt.plot(xco,yco)
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
    image="data:image/jpg;base64," + str(my_base64_jpgData)
    app.run()