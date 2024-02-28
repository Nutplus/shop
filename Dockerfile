# 使用官方的 Python 运行时作为基础镜像
FROM alpine:3.13
RUN apk add ca-certificates

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tencent.com/g' /etc/apk/repositories \
# 安装python3
&& apk add --update --no-cache python3 py3-pip \
&& rm -rf /var/cache/apk/*

# 将当前目录下的所有文件复制到工作目录中
COPY . /app
# 设置工作目录
WORKDIR /app



# 安装依赖到指定的/install文件夹
# 选用国内镜像源以提高下载速度
RUN pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple \
&& pip config set global.trusted-host mirrors.cloud.tencent.com \
&& pip install --upgrade pip \
# pip install scipy 等数学包失败，可使用 apk add py3-scipy 进行， 参考安装 https://pkgs.alpinelinux.org/packages?name=py3-scipy&branch=v3.13
&& pip install --user -r requirements.txt

# 暴露端口。
# 此处端口必须与「服务设置」-「流水线」以及「手动上传代码包」部署时填写的端口一致，否则会部署失败。
EXPOSE 80

# 将所有子文件夹复制到工作目录中
COPY */ /app/


# 将 FastAPI 应用程序运行在端口 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]