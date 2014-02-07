// PixelGrab.cpp : Defines the entry point for the console application.
//

#define _WIN32_WINNT 0x0400
#pragma comment( lib, "user32.lib" )

#include <windows.h>
#include <stdio.h>
#include "stdafx.h"

HHOOK hKeyboardHook;

typedef COLORREF (*GetPixelFuncPtr)(HDC hdc, int x, int y);
bool inFunc = false;

__declspec(dllexport) LRESULT CALLBACK KeyboardEvent (int nCode, WPARAM wParam, LPARAM lParam)
{
    DWORD SHIFT_key=0;
    DWORD CTRL_key=0;
    DWORD ALT_key=0;

	if (inFunc)
		return 0;

	inFunc = true;

    if  ((nCode == HC_ACTION) &&   ((wParam == WM_SYSKEYDOWN) ||  (wParam == WM_KEYDOWN)))      
    {
        KBDLLHOOKSTRUCT hooked_key = *((KBDLLHOOKSTRUCT*)lParam);
        DWORD dwMsg = 1;
        dwMsg += hooked_key.scanCode << 16;
        dwMsg += hooked_key.flags << 24;
        char lpszKeyName[1024] = {0};
        lpszKeyName[0] = '[';

        int i = GetKeyNameTextA(dwMsg,   (lpszKeyName+1),0xFF) + 1;
        lpszKeyName[i] = ']';

        int key = hooked_key.vkCode;
        CTRL_key = GetAsyncKeyState(VK_CONTROL);

		// get pixel under mouse
		if (CTRL_key !=0)
		{
			if (lpszKeyName[1] == '.' )
			{
				FARPROC pGetPixel;

				HINSTANCE _hGDI = LoadLibraryA("gdi32.dll");
				if(_hGDI)
				{
					pGetPixel = GetProcAddress(_hGDI, "GetPixel");
					GetPixelFuncPtr getPixelFunc = reinterpret_cast<GetPixelFuncPtr>( pGetPixel );

					HDC _hdc = GetDC(NULL);
					if(_hdc)
					{
						POINT _cursor;
						GetCursorPos(&_cursor);
						COLORREF _color = getPixelFunc(_hdc, _cursor.x, _cursor.y);
						int _red = GetRValue(_color);
						int _green = GetGValue(_color);
						int _blue = GetBValue(_color);

						// copy to clipboard
						char output[100];
						sprintf(output, "%f, %f, %f", ((float)_red)/255.0f, ((float)_green)/255.0f, ((float)_blue)/255.0f);
						printf("Color: %s\n", output);
						const size_t len = strlen(output) + 1;
						HGLOBAL hMem =  GlobalAlloc(GMEM_MOVEABLE, len);
						memcpy(GlobalLock(hMem), output, len);
						GlobalUnlock(hMem);
						OpenClipboard(0);
						EmptyClipboard();
						SetClipboardData(CF_TEXT, hMem);
						CloseClipboard();
					}
					FreeLibrary(_hGDI);
				}
			}
			//printf("key = %c\n", key);
			//printf("lpszKeyName = %s\n",  lpszKeyName );
		}
        
        CTRL_key = 0;
    }
	inFunc = false;
    return CallNextHookEx(hKeyboardHook,    nCode,wParam,lParam);
}

void MessageLoop()
{
    MSG message;
    while (GetMessage(&message,NULL,0,0)) 
    {
        TranslateMessage( &message );
        DispatchMessage( &message );
    }
}

DWORD WINAPI my_HotKey(LPVOID lpParm)
{
    HINSTANCE hInstance = GetModuleHandle(NULL);
    if (!hInstance) hInstance = LoadLibraryA((LPCSTR) lpParm); 
    if (!hInstance) return 1;

    hKeyboardHook = SetWindowsHookEx (  WH_KEYBOARD_LL, (HOOKPROC) KeyboardEvent,   hInstance,  NULL    );
    MessageLoop();
    UnhookWindowsHookEx(hKeyboardHook);
    return 0;
}

//int main(int argc, char** argv)
int _tmain(int argc, _TCHAR* argv[])
{
    HANDLE hThread;
    DWORD dwThread;

    hThread = CreateThread(NULL,NULL,(LPTHREAD_START_ROUTINE)   my_HotKey, (LPVOID) argv[0], NULL, &dwThread);

    //ShowWindow(FindWindowA("ConsoleWindowClass", NULL), false);

    if (hThread) return WaitForSingleObject(hThread,INFINITE);
    else return 1;

}