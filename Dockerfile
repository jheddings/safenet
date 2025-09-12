# Builder stage - build the safenet application
FROM golang:1.25 AS builder

WORKDIR /app
COPY go.mod go.sum main.go ./
COPY internal/ ./internal/

# Build the application
RUN go mod download

RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o /tmp/safenet .


# Final stage - start with a scratch image to include only the application
FROM scratch

# copy CA certificates for HTTPS requests
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

# install the safenet utility
COPY --from=builder /tmp/safenet /usr/local/bin/safenet

# commands must be presented as an array, otherwise it will be launched
# using a shell, which causes problems handling signals for shutdown
ENTRYPOINT ["/usr/local/bin/safenet"]

# require callers to specify a command
CMD ["--help"]
