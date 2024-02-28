# 使用官方的 Python 运行时作为基础镜像
FROM python:3.9-alpine

# 设置工作目录
WORKDIR /app

# 安装依赖到指定的/install文件夹
# 选用国内镜像源以提高下载速度
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tencent.com/g' /etc/apk/repositories \
    && apk add --update --no-cache ca-certificates \
    && apk add --update --no-cache build-base python3-dev \
    && pip install --upgrade pip \
    && pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple \
    && pip config set global.trusted-host mirrors.cloud.tencent.com \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/cache/apk/*

# 将当前目录下的所有文件复制到工作目录中
COPY . /app

# 设置 uvicorn 的环境变量
ENV UVICORN_WORKERS=4
ENV UVICORN_LOG_LEVEL=info

# 暴露端口。
# 此处端口必须与「服务设置」-「流水线」以及「手动上传代码包」部署时填写的端口一致，否则会部署失败。
EXPOSE 80

# 将 FastAPI 应用程序运行在端口 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "$UVICORN_WORKERS", "--log-level", "$UVICORN_LOG_LEVEL"]
