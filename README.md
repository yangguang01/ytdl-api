# YouTube音频下载API

这是一个使用FastAPI构建的简单YouTube音频下载服务。

## 功能

- 从YouTube下载音频文件（webm格式）
- 支持自定义文件名
- 提供API接口访问下载的文件

## 本地运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行服务：
```bash
uvicorn app.main:app --reload
```

3. 访问API文档：http://127.0.0.1:8000/docs

## 部署

### Google App Engine

```bash
gcloud app deploy app.yaml
```

### Google Cloud Run

```bash
gcloud builds submit --config cloudbuild.yaml
```

## API使用

1. 下载音频：
```bash
curl -X POST "http://localhost:8000/download/" \
     -H "Content-Type: application/json" \
     -d '{"url": "YouTube视频URL", "filename": "test"}'
```

2. 获取音频文件：
```
GET /audio/{filename}.webm
``` 