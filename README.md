# HK1_2627_INT3505E_2

## Cài đặt môi trường

Yêu cầu Python 3.12 trở lên.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Các thư viện cần thiết được khai báo trong [requirements.txt](requirements.txt).
