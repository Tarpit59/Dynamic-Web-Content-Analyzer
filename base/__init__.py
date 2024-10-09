from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'habbd6ag63y628##4#t6&&*89*^%$fGbVGFFnN%5$'

from base.com import controller