from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import yt_dlp
import os
import uuid

app = FastAPI(title="YouTube音频下载服务")

class DownloadRequest(BaseModel):
    url: str
    filename: str = None

@app.post("/download/")
async def download_audio(request: DownloadRequest):
    try:
        # 如果没有提供文件名，生成一个随机文件名
        if not request.filename:
            request.filename = str(uuid.uuid4())
        
        file_path = download_audio_webm(request.url, request.filename)
        
        return {"status": "成功", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"下载失败: {str(e)}")

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail="文件不存在")
    return FileResponse(path=filename)

def download_audio_webm(url: str, custom_filename: str) -> str:
    """
    从指定 URL 下载音频（仅下载 webm 格式的音频流，无转换过程）。

    参数:
        url (str): 媒体资源的 URL。
        custom_filename (str): 下载文件的自定义名称（不含扩展名）。

    返回:
        str: 下载后生成的 webm 文件名。
    """
    outtmpl = f'{custom_filename}.%(ext)s'
    ydl_opts = {
        # 强制只下载 webm 格式的最佳音频流
        'format': 'bestaudio[ext=webm]',
        'outtmpl': outtmpl,
        'quiet': True,
        #'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        },
        'proxy': 'socks5://8t4v58911-region-US-sid-JaboGcGm-t-5:wl34yfx7@us2.cliproxy.io:443',
        #'proxy': 'http://8t4v58911-region-US-sid-JaboGcGm-t-5:wl34yfx7@us2.cliproxy.io:443',
        
        # 强制使用IPv4
        'force_ipv4': True, 
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info)
    
    return file_name

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 