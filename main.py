from fastapi import FastAPI
import requests
import json

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "Momo API đang chạy thành công!",
        "huong_dan": "Truy cập đường dẫn /get-history để lấy lịch sử hoặc /docs để chạy thử nghiệm."
    }

@app.get("/get-history")
def get_momo_history():
    # URL API lấy lịch sử Túi Thần Tài MoMo
    url = "https://api.momo.vn/transis/api/transis/golden-pocket/trans/browse"
    
    # Các Header được trích xuất từ thiết bị của bạn
    headers = {
        "Host": "api.momo.vn",
        "sessionKey": "2a4999b9-882a-48e8-bbb0-d3211cda1b2b",
        "app_code": "5.10.1",
        "userId": "01682962182",
        "user_phone": "01682962182",
        "User-Agent": "MoMoPlatform Store/5.10.1.51001 CFNetwork/1.0 Darwin/25.5.0 (iPhone 13 Pro Max iOS/26.5) AgentID/110335164",
        "lang": "vi",
        "device_performance": "high-end",
        "app_version": "51001",
        "Accept-Encoding": "gzip, deflate, br",
        "channel": "APP",
        "momo-session-key-tracking": "4593B438-40D9-4495-BF5D-A712DC0BBD76",
        "baggage": "sentry-environment=PRODUCTION,sentry-public_key=6e80c9f01f2440c9be5b37606028f996,sentry-release=vn.momo.platform.ios%405.10.1%2B51001,sentry-trace_id=e144b79e2c954518854bea9c592ace44",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyIjoiMDE2ODI5NjIxODIiLCJpbWVpIjoiNTEwMDEtODYyODRhYWQyYjQwYmNlMTI2ZWJlZWY0MzEzOGY0ZjkzMjZlOTgyNTE4ZmMwNmE1NjE2ZDc4OWI4NDJiZDcxYSIsImhJbWVpIjoiOEZiSVBHVkI4dEkyR3BGRWpGeTE5YkxuTGFlSkFSY2lOWERWckRWWGNwWGZtWnUzek1uNE9uNWx5UWdISzByb05FZVZ3cHdFNFRzMjlLTWZsZFlzUEtKNFVtSnRyaVdaVkd2NGlxa0ZqWUU9IiwiTUFQX1NBQ09NX0NBUkQiOjAsIk5BTUUiOiJUcuG6p24gTmjhuq10IEhvw6BuZyIsIkRFVklDRV9PUyI6ImlvcyIsIkFQUF9WRVIiOjUxMDAxLCJhZ2VudF9pZCI6MTEwMzM1MTY0LCJzZXNzaW9uS2V5IjoiREZEMmJOaGpoYllaVzhJRWtkNVNzWStMb3hvUFBGdVpzZzg4V2tZTlJ2ZFZnSHl2YlcvSlR3PT0iLCJ1c2VyX3R5cGUiOjEsImtleSI6Im1vbW8iLCJyYXBpZF9pZCI6IjZXS0pSNkNlMzF1UnlaSjZxSXoybU1vTlcrcUVncVBsZFR3TUFtOTZoSHQxSXA5aEZXbWF1RGttTTREQkthLzFWamFiN1BUOWFKUT0iLCJ1c2Vy_id:110335164",
        "Content-Type": "application/json",
        "sentry-trace": "e144b79e2c954518854bea9c592ace44-008e5004412c4dc2-0",
        "platform-timestamp": "1780862152600",
        "Accept-Language": "vi-VN,vi;q=0.9"
    }
    
    # Request Body mẫu để phân trang lấy lịch sử (Bổ sung thêm nếu ứng dụng yêu cầu tham số khác)
    payload = {
        "offset": 0,
        "limit": 20
    }
    
    try:
        # Gửi request POST lên MoMo
        response = requests.post(url, headers=headers, json=payload)
        
        # Nếu MoMo phản hồi lỗi hệ thống (Ví dụ: Mã HTTP 401, 403, 500...)
        if response.status_code != 200:
            return {
                "error": f"MoMo phản hồi mã lỗi HTTP {response.status_code}",
                "detail": response.text  # Trả về chuỗi lỗi gốc thay vì cố giải mã JSON
            }
            
        # Trả về kết quả JSON lịch sử nếu MoMo xử lý thành công (HTTP 200)
        return response.json()

    except json.JSONDecodeError:
        # Trường hợp MoMo trả về HTTP 200 nhưng nội dung bên trong lại là một trang web lỗi HTML
        return {
            "error": "Phản hồi từ MoMo không phải định dạng JSON hợp lệ.",
            "raw_response": response.text
        }
    except Exception as e:
        # Bắt các lỗi kết nối mạng, timeout...
        return {
            "error": "Đã xảy ra lỗi trong quá trình xử lý request",
            "detail": str(e)
        }
