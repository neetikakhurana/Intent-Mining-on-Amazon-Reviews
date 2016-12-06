import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
from flask import Flask,render_template,url_for
app=Flask(__name__)

"""@app.route('/welcome')
def index():
    return render_template('welcome.html')"""

@app.route('/')
def index():
    return render_template('index.html',product_name = 'Nexus 5x',brand_name = 'Nexus')


if __name__=="__main__":
    app.run()
    
