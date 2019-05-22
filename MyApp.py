from flask import Flask, render_template, request
import SearchEngine,printja,SearchWildcard
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("IR.html")

@app.route('/result', methods=['POST', 'GET'])
def result():
    value = []
    if request.method == "POST":
        word = request.form.get("word")
        word.lower()

        if "*" not in word:
           value,words = SearchEngine.Search_pro(word)
           values = printja.printja(value)
           return render_template("result.html", word=word
                                   , weblink=values ,words=words)
        else:
            value = SearchWildcard.Search_pro_wild(word)
            values = printja.printja(value)
            return render_template("result.html", word=word
                                   , weblink=values)



if __name__ == '__main__':
    app.run(debug=True)