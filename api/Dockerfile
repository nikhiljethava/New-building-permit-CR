# Build stage
FROM golang:1.24-alpine AS build
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
# CGO_ENABLED=1 is required for go-sqlite3
RUN apk add --no-cache gcc musl-dev
RUN CGO_ENABLED=1 GOOS=linux go build -o api-server .

# Run stage
FROM alpine:latest
WORKDIR /app
RUN apk add --no-cache ca-certificates tzdata sqlite
COPY --from=build /app/api-server .
EXPOSE 8080
ENV PORT=8080
ENV DB_NAME=/app/data/building_plans.db
# Create a volume for the sqlite database to persist
VOLUME ["/app/data"]
CMD ["./api-server"]
