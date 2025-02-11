@echo off
:: Đường dẫn file proto
set PROTO_FILE=greeter.proto

:: Di chuyển về thư mục dự án gốc
cd ..

:: Biên dịch file proto
python -m grpc_tools.protoc -I./proto --python_out=./grpc_services --grpc_python_out=./grpc_services ./proto/%PROTO_FILE%

if %errorlevel% equ 0 (
    echo Biên dịch thành công!
) else (
    echo Biên dịch thất bại!
)

pause
