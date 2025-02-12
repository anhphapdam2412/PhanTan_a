# WebApp - Hệ thống Mua Bán

## 1. Giới thiệu
WebApp là một ứng dụng mua bán trực tuyến sử dụng Flask và gRPC để cung cấp các chức năng như đăng nhập, đăng ký, mua bán sản phẩm.

## 2. Cài đặt và Chạy Ứng Dụng
### 2.1 Cài đặt yêu cầu
Trước tiên, bạn cần cài đặt các thư viện yêu cầu bằng cách sử dụng:
```bash
pip install -r requirements.txt
```

### 2.2 Chạy ứng dụng
#### 2.2.1 Mở `app.py` để khởi chạy ứng dụng web:
```bash
python app.py
```
#### 2.2.2 Mở `server.py` để khởi chạy gRPC server:
```bash
python server.py 50051
```
Hoặc nếu có thay đổi cổng:
```bash
python server.py <port>
```

### 2.3 Truy cập ứng dụng
Sau khi khởi động thành công, truy cập địa chỉ:
```
http://127.0.0.1:5000
```

## 3. Chức năng chính
### - Đăng ký tài khoản
- Người dùng có thể đăng ký tài khoản mới bằng cách cung cấp thông tin cần thiết.

### - Đăng nhập
- Hỗ trợ xác thực thông tin người dùng để đăng nhập.

### - Mua bán sản phẩm
- Người dùng có thể duyệt, chọn mua sản phẩm và thực hiện giao dịch.

## 4. Kiểm thử chức năng
Bạn có thể kiểm tra các chức năng chính bằng cách truy cập giao diện web hoặc gửi request API.

## 5. Ghi chú
- Đảm bảo đã cài đặt đầy đủ thư viện trước khi chạy ứng dụng.
- Nếu gặp lỗi, kiểm tra lại kết nối giữa Flask và gRPC server.

## 6. Liên hệ
Nếu có bất kỳ vấn đề hoặc thắc mắc nào, vui lòng liên hệ nhóm phát triển!
