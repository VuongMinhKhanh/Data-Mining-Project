from flask import Flask, render_template, request, jsonify
import pandas as pd
from io import StringIO

from templates.associate.association_rule import create_transactions, show_rules

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/gomcum')
def gomcum():
    return render_template('clustering/gomcum.html')


@app.route('/kethop')
def kethop():
    return render_template('associate/kethop.html')


@app.route('/phanlop')
def phanlop():
    return render_template('classify/phanlop.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    # Check if a file is actually selected
    if file.filename == '':
        return jsonify({"error": "No file provided or filename is empty"}), 400

    # Validate file extension and process
    if file and file.filename.endswith('.txt'):
        # Read the contents of the file
        string_data = file.read().decode('utf-8')

        # Convert string data to StringIO object, then read into pandas DataFrame
        data = StringIO(string_data)
        df = pd.read_csv(data, header=None, dtype=int)

        # print(df.head())

        transactions = create_transactions(df)

        # Collect min_sup and min_conf from the form data
        min_sup = float(request.form["min-sup"]) / 100
        min_conf = float(request.form["min-conf"]) / 100

        try:
            frequent_itemsets, rules = show_rules(transactions, min_sup, min_conf)
            # print(frequent_itemsets.to_dict(orient='records'), rules.to_dict(orient='records'))
            return {
                "frequent_itemsets": frequent_itemsets.to_json(),
                "rules": rules.to_json()
            }
        except ValueError:
            return {
                "frequent_itemsets": jsonify(),
                "rules": jsonify()
            }



if __name__ == '__main__':
    app.run(debug=True)
