#include <Windows.h>
#include <vector>
#include "Source.h"

void(*topython)(int);
unsigned char* ToPixels(HBITMAP BitmapHandle, int& width, int& height);

extern "C" __declspec(dllexport) void start(void(*f)(int)) {
	topython = f;
}

extern "C" __declspec(dllexport) void run() {
	topython(10);
}

extern "C" __declspec(dllexport) unsigned char* take_screenshot(int x, int y, int width, int height) {
	HDC dcScreen = GetDC(0);
	HDC dcTarget = CreateCompatibleDC(dcScreen);
	HBITMAP bmpTarget = CreateCompatibleBitmap(dcScreen, width, height);
	HGDIOBJ oldBmp = SelectObject(dcTarget, bmpTarget);
	BitBlt(dcTarget, 0, 0, width, height, dcScreen, x, y, SRCCOPY | CAPTUREBLT);

    unsigned char* pixels = ToPixels(bmpTarget, width, height);

	SelectObject(dcTarget, oldBmp);
	DeleteObject(bmpTarget);
	DeleteObject(oldBmp);
	DeleteDC(dcTarget);
	DeleteDC(dcScreen);

    return pixels;
}

extern "C" __declspec(dllexport) void freep(unsigned char* p) {
    delete p;
}

unsigned char* ToPixels(HBITMAP BitmapHandle, int& width, int& height)
{
    BITMAP Bmp = { 0 };
    BITMAPINFO Info = { 0 };

    HDC DC = CreateCompatibleDC(NULL);
    std::memset(&Info, 0, sizeof(BITMAPINFO)); //not necessary really..
    HBITMAP OldBitmap = (HBITMAP)SelectObject(DC, BitmapHandle);
    GetObject(BitmapHandle, sizeof(Bmp), &Bmp);

    Info.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    Info.bmiHeader.biWidth = width = Bmp.bmWidth;
    Info.bmiHeader.biHeight = height = Bmp.bmHeight;
    Info.bmiHeader.biPlanes = 1;
    Info.bmiHeader.biBitCount = Bmp.bmBitsPixel;
    Info.bmiHeader.biCompression = BI_RGB;
    Info.bmiHeader.biSizeImage = ((width * Bmp.bmBitsPixel + 31) / 32) * 4 * height;

    unsigned char* pixels = new unsigned char[Info.bmiHeader.biSizeImage];
    GetDIBits(DC, BitmapHandle, 0, height, pixels, &Info, DIB_RGB_COLORS);
    SelectObject(DC, OldBitmap);

    height = std::abs(height);
    DeleteDC(DC);
    return pixels;
}