import argparse
from libs.data_preprocession import *

# Khởi tạo đối tượng ArgumentParser
parser = argparse.ArgumentParser(description='Chương trình Python với tham số địa chỉ.')

# Thêm tham số -a hoặc --address
parser.add_argument('-p', '--pair', help='pair id.')

# Phân tích các tham số từ dòng lệnh
args = parser.parse_args()

# Kiểm tra xem tham số --address đã được cung cấp hay không
if args.pair:
    print("Địa chỉ cần xử lý:", args.pair)
    result = preprocessing(early_predict=7, pair_id=args.pair.strip())
    print(json.dumps(result, indent=1))
else:
    print("Không có địa chỉ được cung cấp.")
    
    