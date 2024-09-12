from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from io import StringIO
import joblib
from sklearn.preprocessing import MinMaxScaler
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


# Đường dẫn tới file .pkl
dt_file_path = '/Users/quytranlx123/Documents/GitHub/Data-Mining-Project/dt_model.pkl'
knn_file_path = '/Users/quytranlx123/Documents/GitHub/Data-Mining-Project/knn_model.pkl'
nb_file_path = '/Users/quytranlx123/Documents/GitHub/Data-Mining-Project/nb_model.pkl'

# Tải scaler đã lưu từ trước
scaler = joblib.load('/Users/quytranlx123/Documents/GitHub/Data-Mining-Project/scaler.pkl')

# Tải mô hình từ file pkl
dt_model = joblib.load(dt_file_path)
knn_model = joblib.load(knn_file_path)
nb_model = joblib.load(nb_file_path)


@app.route('/predict', methods=['POST'])
def predict():
    # Nhận dữ liệu từ người dùng
    data = request.json
    user_input = {
        'Gender': data['gender'],  # Chuyển đổi 1/0 thành 'Male'/'Female'
        'MonthlyIncome': data['income'],  # Số tiền hàng tháng
        'LoanAmount': data['loan'],  # Số tiền vay
        'AgeGroup_1': data['age_group_1'],  # Cột one-hot cho nhóm tuổi 1
        'AgeGroup_2': data['age_group_2'],  # Cột one-hot cho nhóm tuổi 2
        'AgeGroup_3': data['age_group_3'],  # Cột one-hot cho nhóm tuổi 3
        'AgeGroup_4': data['age_group_4']  # Cột one-hot cho nhóm tuổi 4
    }

    # Tạo DataFrame từ dữ liệu người dùng
    X_new = pd.DataFrame([user_input])

    # Đảm bảo rằng DataFrame X_new có cùng số cột như mô hình đã huấn luyện
    for i in range(1, 5):
        if f'AgeGroup_{i}' not in X_new.columns:
            X_new[f'AgeGroup_{i}'] = 0

    # Sắp xếp lại cột để đảm bảo thứ tự đúng
    X_new = X_new[['Gender', 'MonthlyIncome', 'LoanAmount', 'AgeGroup_1', 'AgeGroup_2', 'AgeGroup_3', 'AgeGroup_4']]
    # Chuẩn hóa dữ liệu
    X_new = scaler.transform(X_new)
    print(X_new)
    # Dự đoán
    dt_predictions = dt_model.predict(X_new)
    knn_predictions = knn_model.predict(X_new)
    nb_predictions = nb_model.predict(X_new)

    # Tạo phản hồi
    results = {
        "DecisionTree": "T" if dt_predictions[0] == 1 else "X",
        "KNN": "T" if knn_predictions[0] == 1 else "X",
        "NaiveBayes": "T" if nb_predictions[0] == 1 else "X"
    }

    return jsonify(results)


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
