FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod ./
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o auth-service main.go

FROM gcr.io/distroless/static-debian12
WORKDIR /
COPY --from=builder /app/auth-service /auth-service
EXPOSE 8080
USER nonroot:nonroot
ENTRYPOINT ["/auth-service"]
