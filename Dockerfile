FROM python:3.10.11-alpine as build
WORKDIR /app

RUN pip install pygbag
COPY . .
RUN pygbag --ume_block=0 --build .


FROM nginx
WORKDIR /usr/share/nginx/html
COPY --from=build /app/build/web .
