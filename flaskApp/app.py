from flask import Flask,render_template


app = Flask(__name__)

@app.route("/")
def home():  
    # return "<p>Hello, World!</p>"
    return render_template("index.html")



@app.route("/about")
def about(): 

    return render_template("about.html") 
    # return "<p>i am about</p>"
@app.route("/dashboard/<name>")
def dashboard(name):
    return render_template("dashboard.html",username=name)

if __name__=='__main__':
    app.run(debug=True)
