#include <Windows.h>
#include "Source.h"

extern "C" __declspec(dllexport) unsigned char* take_screenshot(int x, int y, int width, int height) {
	HDC dcScreen = GetDC(0);
	HDC dcTarget = CreateCompatibleDC(dcScreen);
	HBITMAP bmpTarget = CreateCompatibleBitmap(dcScreen, width, height);
	HGDIOBJ oldBmp = SelectObject(dcTarget, bmpTarget);
	BitBlt(dcTarget, 0, 0, width, height, dcScreen, x, y, SRCCOPY);

    BITMAP Bmp = { 0 };
    BITMAPINFO Info = { 0 };
    GetObject(bmpTarget, sizeof(Bmp), &Bmp);

    Info.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    Info.bmiHeader.biWidth = width = Bmp.bmWidth;
    Info.bmiHeader.biHeight = height = Bmp.bmHeight;
    Info.bmiHeader.biPlanes = 1;
    Info.bmiHeader.biBitCount = Bmp.bmBitsPixel;
    Info.bmiHeader.biCompression = BI_RGB;
    Info.bmiHeader.biSizeImage = ((width * Bmp.bmBitsPixel + 31) / 32) * 4 * height;

    unsigned char* pixels = new unsigned char[Info.bmiHeader.biSizeImage];
    GetDIBits(dcTarget, bmpTarget, 0, height, pixels, &Info, DIB_RGB_COLORS);

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