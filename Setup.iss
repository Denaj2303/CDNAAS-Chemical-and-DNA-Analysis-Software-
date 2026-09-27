; DetectiveMode.iss
#define MyAppName "Detective Mode"
#define MyAppVersion "1.0"
#define MyAppExeName "DetectiveMode.exe"

[Setup]
; A unique identifier for your app
AppId={{YOUR-UNIQUE-GUID-HERE}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
; The installer output location
OutputDir=installer
OutputBaseFilename=DetectiveMode_Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
; Require admin privileges to install
PrivilegesRequired=admin

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; This copies your built EXE to the installation folder
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Creates a Start Menu shortcut
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
; Creates a Desktop shortcut (if the task is selected)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Option to launch the app after installation finishes
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent