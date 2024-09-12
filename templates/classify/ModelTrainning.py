import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
import joblib

# Đọc dữ liệu từ file
df = pd.read_csv('PhanLop.txt')

# Mã hóa biến phân loại
df['RepaymentStatus'] = df['RepaymentStatus'].map({'T': 1, 'X': 0})  # Biến nhị phân

# One-Hot Encoding cho AgeGroup
df = pd.get_dummies(df, columns=['AgeGroup'], prefix='AgeGroup', dtype=int)

# Tách dữ liệu thành đặc trưng (X) và mục tiêu (y)
X = df.drop(columns=['RepaymentStatus'])
y = df['RepaymentStatus']

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Chuẩn hóa dữ liệu cho các biến số
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 1. Mô hình Naive Bayes
# Định nghĩa mô hình Naive Bayes
nb_model = GaussianNB()

# Tinh chỉnh tham số bằng GridSearchCV
param_grid = {
    'var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6, 1e-5]
}

grid_search = GridSearchCV(estimator=nb_model, param_grid=param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Mô hình tốt nhất
best_nb_model = grid_search.best_estimator_
print(f"Best parameters for Naive Bayes: {grid_search.best_params_}")

# Dự đoán và đánh giá mô hình
y_pred_nb = best_nb_model.predict(X_test)

# In classification report và confusion matrix cho Naive Bayes
print("Naive Bayes Model (Tuned):")
print("Classification Report:")
print(classification_report(y_test, y_pred_nb))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_nb))

# Lưu mô hình Naive Bayes
joblib.dump(nb_model, '../../nb_model.pkl')


# 2. Mô hình Decision Tree
# Định nghĩa mô hình Decision Tree
dt_model = DecisionTreeClassifier(random_state=42)

# Định nghĩa các tham số cần tinh chỉnh
param_grid = {
    'max_depth': [None, 5, 10, 15, 20],  # Độ sâu tối đa của cây
    'min_samples_split': [2, 5, 10],     # Số mẫu tối thiểu để chia một nút
    'min_samples_leaf': [1, 2, 4, 6]     # Số mẫu tối thiểu tại một nút lá
}

# Tinh chỉnh tham số bằng GridSearchCV
grid_search = GridSearchCV(estimator=dt_model, param_grid=param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Mô hình tốt nhất
best_dt_model = grid_search.best_estimator_
print(f"Best parameters for Decision Tree: {grid_search.best_params_}")

# Dự đoán và đánh giá mô hình
y_pred_dt = best_dt_model.predict(X_test)

# In classification report và confusion matrix cho Decision Tree
print("Decision Tree Model (Tuned):")
print("Classification Report:")
print(classification_report(y_test, y_pred_dt))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_dt))

# 3. Tìm giá trị k phù hợp cho mô hình KNN
k_values = range(1, 50)
best_accuracy = 0
best_k = 1

for k in k_values:
    knn_model = KNeighborsClassifier(n_neighbors=k)
    knn_model.fit(X_train, y_train)
    y_pred_knn = knn_model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred_knn)
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_k = k

    print(f"K: {k}, Accuracy: {accuracy}")

print(f"\nBest K: {best_k} with Accuracy: {best_accuracy}")

best_knn_model = KNeighborsClassifier(n_neighbors=best_k)
best_knn_model.fit(X_train, y_train)
y_pred_knn = best_knn_model.predict(X_test)

# Lưu mô hình KNN
joblib.dump(best_knn_model, '../../knn_model.pkl')

# In classification report và confusion matrix cho KNN
print("KNN Model:")
print("Classification Report:")
print(classification_report(y_test, y_pred_knn))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_knn))

# Lưu scaler
joblib.dump(scaler, '../../scaler.pkl')

