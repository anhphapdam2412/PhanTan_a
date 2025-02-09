@echo off
:: Đường dẫn file proto
set PROTO_FILE=greeter.proto

:: Biên dịch file greeter.proto trong thư mục hiện tại
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. "%PROTO_FILE%"

if %errorlevel% equ 0 (
    echo OK!
) else (
    echo !OK
)

pause
