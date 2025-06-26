# Makefile for CV Processing Project

# Build lại tất cả Docker image (tester, cv_worker,...)
build:
	docker compose build --no-cache

# Chạy test bên trong container tester
test:
	docker compose run --rm tester

# Dọn dẹp toàn bộ container, volume, network
clean:
	docker compose down --volumes --remove-orphans

# Chạy lại toàn bộ từ đầu (clean → build → test)
reset: clean build test

# (Tuỳ chọn) Xem log của worker
logs:
	docker compose logs -f cv_worker

# (Tuỳ chọn) Vào bash container tester
bash:
	docker compose run --rm tester bash

.PHONY: build test clean reset logs bash