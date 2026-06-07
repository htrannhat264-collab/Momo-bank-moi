from fastapi import FastAPI
import requests
import json

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Momo Bank API đang hoạt động ngon lành!"}

@app.get("/get-history")
def get_momo_history():
    # URL lấy từ ảnh mới nhất (03:16)
    url = "https://api.momo.vn/backend/sof/api/SOF_LIST_MANAGER_MSG"
    
    # Cấu hình Headers chuẩn hóa 100% theo ảnh bạn vừa chụp
    headers = {
        "Host": "api.momo.vn",
        "sessionKey": "2a4999b9-882a-48e8-bbb0-d3211cda1b2b",
        "app_code": "5.10.1",
        "MsgType": "SOF_LIST_MANAGER_MSG",
        "user_phone": "01682962182",
        "userId": "01682962182",
        "User-Agent": "MoMoPlatform Store/5.10.1.51001 CFNetwork/1.0 Darwin/25.5.0 (iPhone 13 Pro Max iOS/26.5) AgentID/110335164",
        "lang": "vi",
        "app_version": "51001",
        "device_performance": "high-end",
        "Accept-Encoding": "gzip, deflate, br",
        "channel": "APP",
        "momo-session-key-tracking": "0D9697EF-1861-4E49-B5E2-D775B249DC54",
        "baggage": "sentry-environment=PRODUCTION,sentry-public_key=6e80c9f01f2440c9be5b37606028f996,sentry-release=vn.momo.platform.ios%405.10.1%2B51001,sentry-trace_id=5cbdae3eaa2549e69cded63b8e8ac08d",
        "Connection": "keep-alive",
        
        # Chuỗi token mới dài full từ ảnh 3 sang ảnh 4
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyIjoiMDE2ODI5NjIxODIiLCJpbWVpIjoiNTEwMDEtODYyODRhYWQyYjQwYmNlMTI2ZWJlZWY0MzEzOGY0ZjkzMjZlOTgyNTE4ZmMwNmE1NjE2ZDc4OWI4NDJiZDcxYSIsImhJbWVpIjoiOEZiSVBHVkI4dEkyR3BGRWpGeTE5YkxuTGFlSkFSY2lOWERWckRWWGNwWGZtWnUzek1uNE9uNWx5UWdISzByb05FZVZ3cHdFNFRzMjlLTWZsZFlzUEtKNFVtSnRyaVdaVkd2NGlxa0ZqWUU9IiwiTUFQX1NBQ09NX0NBUkQiOjAsIk5BTUUiOiJUcuG6p24gTmjhuq10IEhvw6BuZyIsIkRFVklDRV9PUyI6ImlvcyIsIkFQUF9WRVIiOjUxMDAxLCJhZ2VudF9pZCI6MTEwMzM1MTY0LCJzZXNzaW9uS2V5IjoiREZEMmJOaGpoYllaVzhJRWtkNVNzWStMb3hvUFBGdVpzZzg4V2tZTlJ2ZFZnSHl2YlcvSlR3PT0iLCJ1c2VyX3R5cGUiOjEsImtleSI6Im1vbW8iLCJyYXBpZF9pZCI6IjZXS0pSNkNlMzF1UnlaSjZxSXoybU1vTlcrcUVncVBsZFR3TUFtOTZoSHQxSXA5aEZXbWF1RGttTTREQkthLzFWamFiN1BUOWFKUT0iLCJ1aWQiOiIwMzgyOTYyMTgyIiwiZXhwIjoxNzgxMjkzNDY5fQ.qI4X_mscD0yM2KuMI_p7pj6-Dz1vQtA_K_2XAzgd8mDNWMXBJm5RrGTgIZmjYrqWsMrb23A-sntQ27tv45jbqEwG5AV-7dgSOeBD5pDL55qV2vUEJTJM25Wm90sGqk3DVu_ELri2Tf7T5fmhdzLJmpWH-YtWk4Tg1mr7gTUkIVvokjt8tT8byh0bgbvvSlo7Nnwk0n5UOZtUfKsOzHvP_zUsAqSB2OuR2qFD20JenL6dTtpckBVdbmZCKsgQkV-ZruUTFrL7TCJHK0AWIBFbjS0bZIaZCHaKiYx2s6KbQPU-miIQE_uZc2-pa50aLMdeKE4GqrayuT8NYxe4SjV9EA",
        
        "timezone": "Asia/Ho_Chi_Minh",
        "env": "production",
        "device_os": "IOS",
        "http-process-timestamp": "1780863320531",
        "app_type": "production",
        "Accept-Charset": "UTF-8",
        "Accept": "application/json",
        "agent_id": "110335164",
        "Content-Type": "application/json",
        "sentry-trace": "5cbdae3eaa2549e69cded63b8e8ac08d-e63f668b08084bb7-0",
        "platform-timestamp": "1780863320532",
        "Accept-Language": "vi-VN,vi;q=0.9"
    }
    
    # Bạn kiểm tra phần "Preview JSON" ở dưới cùng ảnh 4 để điền chính xác object này vào nhé
    payload = {} 
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            return {
                "error": f"MoMo trả về mã lỗi HTTP {response.status_code}",
                "detail": response.text
            }
        return response.json()
        
    except Exception as e:
        return {"error": str(e)}
