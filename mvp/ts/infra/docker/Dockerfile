FROM node:20-slim
WORKDIR /app
COPY mvp/ts /app/mvp/ts
RUN npm --prefix mvp/ts ci || (cd mvp/ts && npm install)
RUN npm --prefix mvp/ts run build
CMD ["node","mvp/ts/dist/main.js"]
