# Đọc dữ liệu từ file 1 và file 2
file1_path = './toado/anh1.txt'
file2_path = './toado/anh2.txt'

file1_coords = []
file2_coords = []

# Đọc file 1
with open(file1_path, 'r') as file1:
    for line in file1:
        x, y = map(int, line.strip().split(','))
        file1_coords.append((x, y))

# Đọc file 2
with open(file2_path, 'r') as file2:
    for line in file2:
        x, y = map(int, line.strip().split(','))
        file2_coords.append((x, y))

# Chỉ sử dụng số lượng điểm ít hơn trong hai tệp
num_points = min(len(file1_coords), len(file2_coords))

diff_x_sum = 0
diff_y_sum = 0

for i in range(num_points):
    x1, y1 = file1_coords[i]
    x2, y2 = file2_coords[i]
    
    diff_x = x1 - x2
    diff_y = y1 - y2
    
    diff_x_sum += diff_x
    diff_y_sum += diff_y

avg_diff_x = diff_x_sum / num_points
avg_diff_y = diff_y_sum / num_points

print(f"Average mark x: {avg_diff_x}")
print(f"Average mark y: {avg_diff_y}")

threshold = 5.0  # Giá trị ngưỡng để xác thực

# Xác thực
if abs(avg_diff_x) < threshold and abs(avg_diff_y) < threshold:
    print("✅ Authentication successful: Two faces match!")
else:
    print("❌ Authentication failed: Two different faces!")
