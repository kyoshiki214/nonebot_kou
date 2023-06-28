FROM mcr.microsoft.com/playwright:v1.22.0-focal

WORKDIR /app

RUN apt update && apt install -y python3.9 python3-pip \
    libzbar-dev locales locales-all fonts-noto libnss3-dev \
    libxss1 libasound2 libxrandr2 libatk1.0-0 libgtk-3-0 libgbm-dev libxshmfence1

RUN rm -rf /usr/bin/python3 && ln -s /usr/bin/python3.9 /usr/bin/python \
    && ln -s /usr/bin/python3.9 /usr/bin/python3

ENV TZ=Asia/Shanghai

RUN echo "${TZ}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime \
    && apt install -y tzdata \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt --no-dependencies

RUN rm requirements.txt

RUN nb plugin install nonebot_plugin_chatgpt_on_qq

COPY ./ /app/

EXPOSE 8080

CMD ["nb","run"]
