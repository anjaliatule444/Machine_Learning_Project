from flask import Flask,request,app

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    return "Hello Varad"

if __name__ == "__main__":
    app.run(debug=True)