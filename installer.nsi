; Script generated by the HM NIS Edit Script Wizard.

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "������ �����������"
!define PRODUCT_VERSION "1.0"
!define PRODUCT_PUBLISHER "AlexDev"
!define PRODUCT_WEB_SITE "https://github.com/AlexDev-py/Thermometry-Log"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\ThermometryLog.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

SetCompressor lzma

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "icon.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\orange-uninstall.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; Components page
!insertmacro MUI_PAGE_COMPONENTS
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\ThermometryLog.exe"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "Russian"

; Reserve files
!insertmacro MUI_RESERVEFILE_INSTALLOPTIONS

; MUI end ------

Name "${PRODUCT_NAME}"
OutFile "build\installers\ThermometryLogSetup.exe"
InstallDir "$PROGRAMFILES\������ �����������"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Section "WebView2" SEC02
  SetOutPath "$INSTDIR"
  File "build\installers\MicrosoftEdgeWebview2Setup.exe"
  ExecWait "$INSTDIR\MicrosoftEdgeWebview2Setup.exe"
  Delete "$INSTDIR\MicrosoftEdgeWebview2Setup.exe"
SectionEnd

Section "������ �����������" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite try
  File "build\ThermometryLog\csv_handler.py"
  File "build\ThermometryLog\database.py"
  File "build\ThermometryLog\excel.py"
  SetOutPath "$INSTDIR\lib"
  File "build\ThermometryLog\lib\clr.pyd"
  SetOutPath "$INSTDIR\lib\jinja2"
  File "build\ThermometryLog\lib\jinja2\asyncfilters.pyc"
  File "build\ThermometryLog\lib\jinja2\asyncsupport.pyc"
  File "build\ThermometryLog\lib\jinja2\bccache.pyc"
  File "build\ThermometryLog\lib\jinja2\compiler.pyc"
  File "build\ThermometryLog\lib\jinja2\constants.pyc"
  File "build\ThermometryLog\lib\jinja2\debug.pyc"
  File "build\ThermometryLog\lib\jinja2\defaults.pyc"
  File "build\ThermometryLog\lib\jinja2\environment.pyc"
  File "build\ThermometryLog\lib\jinja2\exceptions.pyc"
  File "build\ThermometryLog\lib\jinja2\ext.pyc"
  File "build\ThermometryLog\lib\jinja2\filters.pyc"
  File "build\ThermometryLog\lib\jinja2\idtracking.pyc"
  File "build\ThermometryLog\lib\jinja2\lexer.pyc"
  File "build\ThermometryLog\lib\jinja2\loaders.pyc"
  File "build\ThermometryLog\lib\jinja2\meta.pyc"
  File "build\ThermometryLog\lib\jinja2\nativetypes.pyc"
  File "build\ThermometryLog\lib\jinja2\nodes.pyc"
  File "build\ThermometryLog\lib\jinja2\optimizer.pyc"
  File "build\ThermometryLog\lib\jinja2\parser.pyc"
  File "build\ThermometryLog\lib\jinja2\runtime.pyc"
  File "build\ThermometryLog\lib\jinja2\sandbox.pyc"
  File "build\ThermometryLog\lib\jinja2\tests.pyc"
  File "build\ThermometryLog\lib\jinja2\utils.pyc"
  File "build\ThermometryLog\lib\jinja2\visitor.pyc"
  File "build\ThermometryLog\lib\jinja2\_compat.pyc"
  File "build\ThermometryLog\lib\jinja2\_identifier.pyc"
  File "build\ThermometryLog\lib\jinja2\__init__.pyc"
  SetOutPath "$INSTDIR\lib"
  File "build\ThermometryLog\lib\libcrypto-1_1.dll"
  File "build\ThermometryLog\lib\libffi-7.dll"
  File "build\ThermometryLog\lib\library.zip"
  File "build\ThermometryLog\lib\libssl-1_1.dll"
  SetOutPath "$INSTDIR\lib\markupsafe"
  File "build\ThermometryLog\lib\markupsafe\python38.dll"
  File "build\ThermometryLog\lib\markupsafe\vcruntime140.dll"
  File "build\ThermometryLog\lib\markupsafe\_compat.pyc"
  File "build\ThermometryLog\lib\markupsafe\_constants.pyc"
  File "build\ThermometryLog\lib\markupsafe\_native.pyc"
  File "build\ThermometryLog\lib\markupsafe\_speedups.cp38-win_amd64.pyd"
  File "build\ThermometryLog\lib\markupsafe\__init__.pyc"
  SetOutPath "$INSTDIR\lib"
  File "build\ThermometryLog\lib\pyexpat.pyd"
  File "build\ThermometryLog\lib\Python.Runtime.dll"
  File "build\ThermometryLog\lib\select.pyd"
  File "build\ThermometryLog\lib\sqlite3.dll"
  File "build\ThermometryLog\lib\unicodedata.pyd"
  SetOutPath "$INSTDIR\lib\webview"
  File "build\ThermometryLog\lib\webview\event.pyc"
  File "build\ThermometryLog\lib\webview\guilib.pyc"
  SetOutPath "$INSTDIR\lib\webview\js"
  File "build\ThermometryLog\lib\webview\js\alert.pyc"
  File "build\ThermometryLog\lib\webview\js\api.pyc"
  File "build\ThermometryLog\lib\webview\js\css.pyc"
  File "build\ThermometryLog\lib\webview\js\dom.pyc"
  File "build\ThermometryLog\lib\webview\js\drag.pyc"
  File "build\ThermometryLog\lib\webview\js\event.pyc"
  File "build\ThermometryLog\lib\webview\js\npo.pyc"
  File "build\ThermometryLog\lib\webview\js\__init__.pyc"
  SetOutPath "$INSTDIR\lib\webview\lib"
  File "build\ThermometryLog\lib\webview\lib\Microsoft.Toolkit.Forms.UI.Controls.WebView.dll"
  File "build\ThermometryLog\lib\webview\lib\Microsoft.Toolkit.Forms.UI.Controls.WebView.LICENSE.md"
  File "build\ThermometryLog\lib\webview\lib\Microsoft.Web.WebView2.Core.dll"
  File "build\ThermometryLog\lib\webview\lib\Microsoft.Web.WebView2.LICENSE.md"
  File "build\ThermometryLog\lib\webview\lib\Microsoft.Web.WebView2.WinForms.dll"
  File "build\ThermometryLog\lib\webview\lib\WebBrowserInterop.x64.dll"
  File "build\ThermometryLog\lib\webview\lib\WebBrowserInterop.x86.dll"
  SetOutPath "$INSTDIR\lib\webview\lib\x64"
  File "build\ThermometryLog\lib\webview\lib\x64\WebView2Loader.dll"
  SetOutPath "$INSTDIR\lib\webview\lib\x86"
  File "build\ThermometryLog\lib\webview\lib\x86\WebView2Loader.dll"
  SetOutPath "$INSTDIR\lib\webview"
  File "build\ThermometryLog\lib\webview\localization.pyc"
  SetOutPath "$INSTDIR\lib\webview\platforms"
  File "build\ThermometryLog\lib\webview\platforms\cef.pyc"
  File "build\ThermometryLog\lib\webview\platforms\cocoa.pyc"
  File "build\ThermometryLog\lib\webview\platforms\edgechromium.pyc"
  File "build\ThermometryLog\lib\webview\platforms\edgehtml.pyc"
  File "build\ThermometryLog\lib\webview\platforms\gtk.pyc"
  File "build\ThermometryLog\lib\webview\platforms\mshtml.pyc"
  File "build\ThermometryLog\lib\webview\platforms\qt.pyc"
  File "build\ThermometryLog\lib\webview\platforms\winforms.pyc"
  File "build\ThermometryLog\lib\webview\platforms\__init__.pyc"
  SetOutPath "$INSTDIR\lib\webview"
  File "build\ThermometryLog\lib\webview\serving.pyc"
  File "build\ThermometryLog\lib\webview\util.pyc"
  File "build\ThermometryLog\lib\webview\window.pyc"
  File "build\ThermometryLog\lib\webview\wsgi.pyc"
  File "build\ThermometryLog\lib\webview\__init__.pyc"
  SetOutPath "$INSTDIR\lib"
  File "build\ThermometryLog\lib\_bz2.pyd"
  File "build\ThermometryLog\lib\_ctypes.pyd"
  File "build\ThermometryLog\lib\_decimal.pyd"
  File "build\ThermometryLog\lib\_elementtree.pyd"
  File "build\ThermometryLog\lib\_hashlib.pyd"
  File "build\ThermometryLog\lib\_lzma.pyd"
  File "build\ThermometryLog\lib\_multiprocessing.pyd"
  File "build\ThermometryLog\lib\_queue.pyd"
  File "build\ThermometryLog\lib\_socket.pyd"
  File "build\ThermometryLog\lib\_sqlite3.pyd"
  File "build\ThermometryLog\lib\_ssl.pyd"
  SetOutPath "$INSTDIR"
  File "build\ThermometryLog\logger.py"
  File "build\ThermometryLog\main.py"
  File "build\ThermometryLog\python3.dll"
  File "build\ThermometryLog\python38.dll"
  File "build\ThermometryLog\ThermometryLog.exe"
  CreateDirectory "$SMPROGRAMS\������ �����������"
  CreateShortCut "$SMPROGRAMS\������ �����������\������ �����������.lnk" "$INSTDIR\ThermometryLog.exe"
  CreateShortCut "$DESKTOP\������ �����������.lnk" "$INSTDIR\ThermometryLog.exe"
  File "build\ThermometryLog\vcruntime140.dll"
  SetOutPath "$INSTDIR\web"
  File "build\ThermometryLog\web\app.py"
  SetOutPath "$INSTDIR\web\static\css"
  File "build\ThermometryLog\web\static\css\dark_color_scheme.css"
  File "build\ThermometryLog\web\static\css\default_color_scheme.css"
  File "build\ThermometryLog\web\static\css\light_color_scheme.css"
  File "build\ThermometryLog\web\static\css\main.css"
  SetOutPath "$INSTDIR\web\static"
  File "build\ThermometryLog\web\static\logo.png"
  SetOutPath "$INSTDIR\web\templates"
  File "build\ThermometryLog\web\templates\base.html"
  File "build\ThermometryLog\web\templates\main.html"
  File "build\ThermometryLog\web\templates\search_base.html"
  File "build\ThermometryLog\web\templates\search_name.html"
  File "build\ThermometryLog\web\templates\search_temp.html"
  SetOutPath "$INSTDIR\web\__pycache__"
  File "build\ThermometryLog\web\__pycache__\app.cpython-38.pyc"
  SetOutPath "$INSTDIR\__pycache__"
  File "build\ThermometryLog\__pycache__\csv_handler.cpython-38.pyc"
  File "build\ThermometryLog\__pycache__\database.cpython-38.pyc"
  File "build\ThermometryLog\__pycache__\excel.cpython-38.pyc"
  File "build\ThermometryLog\__pycache__\logger.cpython-38.pyc"
  File "build\ThermometryLog\__pycache__\main.cpython-38.pyc"
  SetOutPath "$LocalAppData\ThermometryLog"
  SetOverwrite ifnewer
  File "build\sources\database.sqlite"
  File "build\sources\logs.log"
  File "build\sources\settings.json"
SectionEnd

Section -AdditionalIcons
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateShortCut "$SMPROGRAMS\������ �����������\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\ThermometryLog.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\ThermometryLog.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd

; Section descriptions
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC01} "����������."
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC02} "Microsoft Edge WebView2. �������, ����������� ��� ������ ����������."
!insertmacro MUI_FUNCTION_DESCRIPTION_END


Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "�������� ��������� $(^Name) ���� ������� ���������."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "�� ������� � ���, ��� ������� ������� $(^Name) � ��� ���������� ���������?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$INSTDIR\${PRODUCT_NAME}.url"
  Delete "$INSTDIR\uninst.exe"
  Delete "$INSTDIR\MicrosoftEdgeWebview2Setup.exe"
  Delete "$LocalAppData\ThermometryLog\settings.json"
  Delete "$LocalAppData\ThermometryLog\logs.log"
  Delete "$LocalAppData\ThermometryLog\database.sqlite"
  Delete "$INSTDIR\__pycache__\main.cpython-38.pyc"
  Delete "$INSTDIR\__pycache__\logger.cpython-38.pyc"
  Delete "$INSTDIR\__pycache__\excel.cpython-38.pyc"
  Delete "$INSTDIR\__pycache__\database.cpython-38.pyc"
  Delete "$INSTDIR\__pycache__\csv_handler.cpython-38.pyc"
  Delete "$INSTDIR\web\__pycache__\app.cpython-38.pyc"
  Delete "$INSTDIR\web\templates\search_temp.html"
  Delete "$INSTDIR\web\templates\search_name.html"
  Delete "$INSTDIR\web\templates\search_base.html"
  Delete "$INSTDIR\web\templates\main.html"
  Delete "$INSTDIR\web\templates\base.html"
  Delete "$INSTDIR\web\static\logo.png"
  Delete "$INSTDIR\web\static\css\main.css"
  Delete "$INSTDIR\web\static\css\light_color_scheme.css"
  Delete "$INSTDIR\web\static\css\default_color_scheme.css"
  Delete "$INSTDIR\web\static\css\dark_color_scheme.css"
  Delete "$INSTDIR\web\app.py"
  Delete "$INSTDIR\vcruntime140.dll"
  Delete "$INSTDIR\ThermometryLog.exe"
  Delete "$INSTDIR\python38.dll"
  Delete "$INSTDIR\python3.dll"
  Delete "$INSTDIR\main.py"
  Delete "$INSTDIR\logger.py"
  Delete "$INSTDIR\lib\_ssl.pyd"
  Delete "$INSTDIR\lib\_sqlite3.pyd"
  Delete "$INSTDIR\lib\_socket.pyd"
  Delete "$INSTDIR\lib\_queue.pyd"
  Delete "$INSTDIR\lib\_multiprocessing.pyd"
  Delete "$INSTDIR\lib\_lzma.pyd"
  Delete "$INSTDIR\lib\_hashlib.pyd"
  Delete "$INSTDIR\lib\_elementtree.pyd"
  Delete "$INSTDIR\lib\_decimal.pyd"
  Delete "$INSTDIR\lib\_ctypes.pyd"
  Delete "$INSTDIR\lib\_bz2.pyd"
  Delete "$INSTDIR\lib\webview\__init__.pyc"
  Delete "$INSTDIR\lib\webview\wsgi.pyc"
  Delete "$INSTDIR\lib\webview\window.pyc"
  Delete "$INSTDIR\lib\webview\util.pyc"
  Delete "$INSTDIR\lib\webview\serving.pyc"
  Delete "$INSTDIR\lib\webview\platforms\__init__.pyc"
  Delete "$INSTDIR\lib\webview\platforms\winforms.pyc"
  Delete "$INSTDIR\lib\webview\platforms\qt.pyc"
  Delete "$INSTDIR\lib\webview\platforms\mshtml.pyc"
  Delete "$INSTDIR\lib\webview\platforms\gtk.pyc"
  Delete "$INSTDIR\lib\webview\platforms\edgehtml.pyc"
  Delete "$INSTDIR\lib\webview\platforms\edgechromium.pyc"
  Delete "$INSTDIR\lib\webview\platforms\cocoa.pyc"
  Delete "$INSTDIR\lib\webview\platforms\cef.pyc"
  Delete "$INSTDIR\lib\webview\localization.pyc"
  Delete "$INSTDIR\lib\webview\lib\x86\WebView2Loader.dll"
  Delete "$INSTDIR\lib\webview\lib\x64\WebView2Loader.dll"
  Delete "$INSTDIR\lib\webview\lib\WebBrowserInterop.x86.dll"
  Delete "$INSTDIR\lib\webview\lib\WebBrowserInterop.x64.dll"
  Delete "$INSTDIR\lib\webview\lib\Microsoft.Web.WebView2.WinForms.dll"
  Delete "$INSTDIR\lib\webview\lib\Microsoft.Web.WebView2.LICENSE.md"
  Delete "$INSTDIR\lib\webview\lib\Microsoft.Web.WebView2.Core.dll"
  Delete "$INSTDIR\lib\webview\lib\Microsoft.Toolkit.Forms.UI.Controls.WebView.LICENSE.md"
  Delete "$INSTDIR\lib\webview\lib\Microsoft.Toolkit.Forms.UI.Controls.WebView.dll"
  Delete "$INSTDIR\lib\webview\js\__init__.pyc"
  Delete "$INSTDIR\lib\webview\js\npo.pyc"
  Delete "$INSTDIR\lib\webview\js\event.pyc"
  Delete "$INSTDIR\lib\webview\js\drag.pyc"
  Delete "$INSTDIR\lib\webview\js\dom.pyc"
  Delete "$INSTDIR\lib\webview\js\css.pyc"
  Delete "$INSTDIR\lib\webview\js\api.pyc"
  Delete "$INSTDIR\lib\webview\js\alert.pyc"
  Delete "$INSTDIR\lib\webview\guilib.pyc"
  Delete "$INSTDIR\lib\webview\event.pyc"
  Delete "$INSTDIR\lib\unicodedata.pyd"
  Delete "$INSTDIR\lib\sqlite3.dll"
  Delete "$INSTDIR\lib\select.pyd"
  Delete "$INSTDIR\lib\Python.Runtime.dll"
  Delete "$INSTDIR\lib\pyexpat.pyd"
  Delete "$INSTDIR\lib\markupsafe\__init__.pyc"
  Delete "$INSTDIR\lib\markupsafe\_speedups.cp38-win_amd64.pyd"
  Delete "$INSTDIR\lib\markupsafe\_native.pyc"
  Delete "$INSTDIR\lib\markupsafe\_constants.pyc"
  Delete "$INSTDIR\lib\markupsafe\_compat.pyc"
  Delete "$INSTDIR\lib\markupsafe\vcruntime140.dll"
  Delete "$INSTDIR\lib\markupsafe\python38.dll"
  Delete "$INSTDIR\lib\libssl-1_1.dll"
  Delete "$INSTDIR\lib\library.zip"
  Delete "$INSTDIR\lib\libffi-7.dll"
  Delete "$INSTDIR\lib\libcrypto-1_1.dll"
  Delete "$INSTDIR\lib\jinja2\__init__.pyc"
  Delete "$INSTDIR\lib\jinja2\_identifier.pyc"
  Delete "$INSTDIR\lib\jinja2\_compat.pyc"
  Delete "$INSTDIR\lib\jinja2\visitor.pyc"
  Delete "$INSTDIR\lib\jinja2\utils.pyc"
  Delete "$INSTDIR\lib\jinja2\tests.pyc"
  Delete "$INSTDIR\lib\jinja2\sandbox.pyc"
  Delete "$INSTDIR\lib\jinja2\runtime.pyc"
  Delete "$INSTDIR\lib\jinja2\parser.pyc"
  Delete "$INSTDIR\lib\jinja2\optimizer.pyc"
  Delete "$INSTDIR\lib\jinja2\nodes.pyc"
  Delete "$INSTDIR\lib\jinja2\nativetypes.pyc"
  Delete "$INSTDIR\lib\jinja2\meta.pyc"
  Delete "$INSTDIR\lib\jinja2\loaders.pyc"
  Delete "$INSTDIR\lib\jinja2\lexer.pyc"
  Delete "$INSTDIR\lib\jinja2\idtracking.pyc"
  Delete "$INSTDIR\lib\jinja2\filters.pyc"
  Delete "$INSTDIR\lib\jinja2\ext.pyc"
  Delete "$INSTDIR\lib\jinja2\exceptions.pyc"
  Delete "$INSTDIR\lib\jinja2\environment.pyc"
  Delete "$INSTDIR\lib\jinja2\defaults.pyc"
  Delete "$INSTDIR\lib\jinja2\debug.pyc"
  Delete "$INSTDIR\lib\jinja2\constants.pyc"
  Delete "$INSTDIR\lib\jinja2\compiler.pyc"
  Delete "$INSTDIR\lib\jinja2\bccache.pyc"
  Delete "$INSTDIR\lib\jinja2\asyncsupport.pyc"
  Delete "$INSTDIR\lib\jinja2\asyncfilters.pyc"
  Delete "$INSTDIR\lib\clr.pyd"
  Delete "$INSTDIR\excel.py"
  Delete "$INSTDIR\database.py"
  Delete "$INSTDIR\csv_handler.py"

  Delete "$SMPROGRAMS\������ �����������\Uninstall.lnk"
  Delete "$SMPROGRAMS\������ �����������\Website.lnk"
  Delete "$DESKTOP\������ �����������.lnk"
  Delete "$SMPROGRAMS\������ �����������\������ �����������.lnk"

  RMDir "$SMPROGRAMS\������ �����������"
  RMDir "$INSTDIR\web\templates"
  RMDir "$INSTDIR\web\static\css"
  RMDir "$INSTDIR\web\static"
  RMDir "$INSTDIR\web\__pycache__"
  RMDir "$INSTDIR\web"
  RMDir "$INSTDIR\lib\webview\platforms"
  RMDir "$INSTDIR\lib\webview\lib\x86"
  RMDir "$INSTDIR\lib\webview\lib\x64"
  RMDir "$INSTDIR\lib\webview\lib"
  RMDir "$INSTDIR\lib\webview\js"
  RMDir "$INSTDIR\lib\webview"
  RMDir "$INSTDIR\lib\markupsafe"
  RMDir "$INSTDIR\lib\jinja2"
  RMDir "$INSTDIR\lib"
  RMDir "$INSTDIR\__pycache__"
  RMDir "$INSTDIR"
  RMDir "$LocalAppData\ThermometryLog"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd