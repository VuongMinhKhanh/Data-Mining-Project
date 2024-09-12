import random
import pandas as pd

# Các thông số cho dữ liệu mẫu
genders = [0, 1]  # 0: Nữ, 1: Nam
age_groups = [1, 2, 3, 4]  # 1: 18-25, 2: 26-35, 3: 36-50, 4: trên 51 tuổi
status = ['T', 'X']  # T: Tốt, X: Xấu

# Tạo dữ liệu mẫu dựa trên thực tế
data_samples = []
for _ in range(10000):  # Số lượng dòng dữ liệu
    gender = random.choice(genders)
    age_group = random.choice(age_groups)

    # Thu nhập hàng tháng dựa trên nhóm tuổi
    if age_group == 1:  # 18-25 tuổi
        income = random.randint(5, 20)  # Thu nhập từ 5 đến 20 triệu
    elif age_group == 2:  # 26-35 tuổi
        income = random.randint(15, 50)  # Thu nhập từ 15 đến 50 triệu
    elif age_group == 3:  # 36-50 tuổi
        income = random.randint(20, 80)  # Thu nhập từ 20 đến 80 triệu
    else:  # Trên 51 tuổi
        income = random.randint(15, 60)  # Thu nhập từ 15 đến 60 triệu

    # Tạo trường hợp ngoại suy cho MonthlyIncome (khoảng 5% các trường hợp có thu nhập vượt trên 100 triệu)
    if random.random() < 0.05:
        income = random.randint(101, 200)  # Ngoại suy thu nhập từ 101 đến 200 triệu

    # Số tiền vay
    loan_amount = random.randint(50, 500)  # Số tiền vay từ 50 đến 500 triệu

    # Tạo trường hợp ngoại suy cho LoanAmount (khoảng 3% các trường hợp có khoản vay trên 500 triệu)
    if random.random() < 0.03:
        loan_amount = random.randint(501, 1000)  # Ngoại suy từ 501 đến 1000 triệu

    # Tính tỷ lệ giữa income và loan_amount
    ratio = income / loan_amount

    # Tình trạng trả nợ dựa trên tỷ lệ
    if ratio < 0.2:  # Nếu tỷ lệ nhỏ hơn 0.2, tình trạng sẽ là xấu
        repayment_status = 'X'  # Xấu
    else:
        repayment_status = 'T'  # Tốt nếu tỷ lệ >= 0.2

    # Thêm dữ liệu mẫu vào danh sách
    data_samples.append(f"{gender},{age_group},{income},{loan_amount},{repayment_status}")

# Thêm tên các cột vào tệp tin
header = "Gender,AgeGroup,MonthlyIncome,LoanAmount,RepaymentStatus\n"

# Lưu vào tệp tin PhanLopThucTe.txt
with open('PhanLop.txt', 'w') as f:
    f.write(header)  # Ghi tên các cột
    f.write('\n'.join(data_samples))  # Ghi dữ liệu mẫu

# Đọc dữ liệu từ tệp tin vào DataFrame
df = pd.read_csv('PhanLop.txt')

# Hiển thị DataFrame
print("Dữ liệu thực tế đã tạo:")
print(df.head())
