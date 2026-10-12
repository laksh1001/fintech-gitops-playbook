FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod ./
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o notification-service main.go

FROM gcr.io/distroless/static-debian12
WORKDIR /
COPY --from=builder /app/notification-service /notification-service
EXPOSE 8082
USER nonroot:nonroot
ENTRYPOINT ["/notification-service"]
