#pragma once

extern "C" __declspec(dllexport) void start(void(*f)(int));
extern "C" __declspec(dllexport) void run();
extern "C" __declspec(dllexport) unsigned char* take_screenshot(int x, int y, int width, int height);
extern "C" __declspec(dllexport) void freep(unsigned char* p);