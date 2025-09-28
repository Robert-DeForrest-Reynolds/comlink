# Minimal cross-platform Makefile
# Run `make all` to build everything
# Requires cross-compilers installed on Linux

SRC = comlink.c
BIN = bin

# Ensure bin directory exists
$(BIN):
	mkdir -p $(BIN)

# Linux builds
linux-x64: $(BIN)
	gcc $(SRC) -o $(BIN)/mytool-linux-x64

linux-arm64: $(BIN)
	aarch64-linux-gnu-gcc $(SRC) -o $(BIN)/mytool-linux-arm64

# Windows builds (cross via MinGW)
windows-x64: $(BIN)
	x86_64-w64-mingw32-gcc $(SRC) -o $(BIN)/mytool-windows-x64.exe

windows-arm64: $(BIN)
	aarch64-w64-mingw32-gcc $(SRC) -o $(BIN)/mytool-windows-arm64.exe

# macOS builds (requires osxcross)
macos-x64: $(BIN)
	o64-clang $(SRC) -o $(BIN)/mytool-macos-x64

macos-arm64: $(BIN)
	o64-clang -arch arm64 $(SRC) -o $(BIN)/mytool-macos-arm64

# Build everything
all: linux-x64 linux-arm64 windows-x64 windows-arm64 macos-x64 macos-arm64

# Cleanup
clean:
	rm -rf $(BIN)
