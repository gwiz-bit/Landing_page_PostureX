"""Chuyển lỗi kiểm tra dữ liệu (HTTP 422) thành MỘT câu tiếng Việt cho người dùng.

FastAPI/Pydantic trả `detail` là một DANH SÁCH đối tượng ({"type", "loc", "msg", ...}).
Các trang web đọc `detail` như chuỗi nên nếu để nguyên sẽ hiện "[object Object]".
"""

GENERIC_INVALID = "Dữ liệu không hợp lệ. Vui lòng kiểm tra lại các ô đã nhập."

# Pydantic gắn tiền tố này vào thông báo do `raise ValueError("...")` trong validator
# tự viết (vd quy tắc mật khẩu của backend app). Các thông báo đó đã là tiếng Việt, đọc
# được — còn thông báo có sẵn của Pydantic (tiếng Anh, vd "String should have at least...")
# thì không đưa cho người dùng.
_CUSTOM_PREFIX = "Value error, "


def friendly_validation_detail(errors) -> str:
    """`errors`: danh sách lỗi của Pydantic (hoặc bất kỳ thứ gì backend app gửi sang)."""
    messages: list[str] = []
    if isinstance(errors, list):
        for item in errors:
            msg = item.get("msg") if isinstance(item, dict) else None
            if isinstance(msg, str) and msg.startswith(_CUSTOM_PREFIX):
                text = msg[len(_CUSTOM_PREFIX):].strip()
                if text and text not in messages:
                    messages.append(text)
    return " ".join(messages) if messages else GENERIC_INVALID
