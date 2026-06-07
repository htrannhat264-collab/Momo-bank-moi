from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests
import json

# Khởi tạo ứng dụng FastAPI với tài liệu tiếng Việt
app = FastAPI(
    title="Hệ thống API kết nối MoMo",
    description="Ứng dụng trung gian lấy thông tin tài khoản và số dư ví MoMo.",
    version="1.0.0"
)

@app.get("/", summary="Trang chủ")
def home():
    return JSONResponse(
        content={
            "trang_thai": "Hệ thống đang hoạt động ổn định!",
            "huong_dan": "Bản hãy truy cập đường dẫn /docs trên trình duyệt để nhập Token mới và chạy thử."
        },
        headers={"Content-Type": "application/json; charset=utf-8"}
    )

@app.get("/get-balance", summary="Lấy thông tin số dư ví")
def get_momo_balance(
    auth_token: str = Query(
        ..., 
        description="Điền chuỗi mã Authorization (Bearer eyJ0eX...) mới nhất bắt được từ điện thoại."
    ),
    session_key: str = Query(
        "2a4999b9-882a-48e8-bbb0-d3211cda1b2b", 
        description="Mã khóa phiên làm việc (sessionKey) của tài khoản."
    ),
    session_tracking: str = Query(
        "0D9697EF-1861-4E49-B5E2-D775B249DC54", 
        description="Mã định danh theo dõi thiết bị (momo-session-key-tracking)."
    )
):
    # Đường dẫn API lấy danh sách nguồn tiền từ MoMo
    url = "https://api.momo.vn/backend/sof/api/SOF_LIST_MANAGER_MSG"
    
    # Cấu hình Headers giả lập thiết bị iPhone của bạn
    headers = {
        "Host": "api.momo.vn",
        "sessionKey": session_key,
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
        "momo-session-key-tracking": session_tracking,
        "baggage": "sentry-environment=PRODUCTION,sentry-public_key=6e80c9f01f2440c9be5b37606028f996,sentry-release=vn.momo.platform.ios%405.10.1%2B51001,sentry-trace_id=5cbdae3eaa2549e69cded63b8e8ac08d",
        "Connection": "keep-alive",
        "Authorization": auth_token,  # Nhận token động truyền vào từ trình duyệt
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
    
    payload = {} 
    
    try:
        # Gửi yêu cầu đến máy chủ MoMo
        response = requests.post(url, headers=headers, json=payload)
        
        # Nếu MoMo trả về mã lỗi (Ví dụ: 401 hết hạn token, 403 bị chặn...)
        if response.status_code != 200:
            return JSONResponse(
                status_code=400,
                content={
                    "ket_qua": "Thất bại",
                    "loi": f"Máy chủ MoMo phản hồi mã lỗi HTTP {response.status_code}",
                    "chi_tiet": response.text
                },
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
            
        # Trả về kết quả thành công và hiển thị dữ liệu tiếng Việt chuẩn
        return JSONResponse(
            content={
                "ket_qua": "Thành công",
                "du_lieu": response.json()
            },
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
    except json.JSONDecodeError:
        return JSONResponse(
            status_code=500,
            content={
                "ket_qua": "Thất bại",
                "loi": "Phản hồi từ MoMo không đúng định dạng dữ liệu JSON.",
                "phan_hoi_goc": response.text
            },
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "ket_qua": "Thất bại",
                "loi": "Đã xảy ra lỗi trong quá trình xử lý kết nối",
                "chi_tiet": str(e)
            },
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
