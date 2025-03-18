[Setup]
AppName=Libelula Softwares
AppVersion=1.0
DefaultDirName={pf}\Libelula Softwares
DefaultGroupName=Libelula Softwares
OutputDir=build
OutputBaseFilename=Libelula Softwares Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "banco\*"; DestDir: "{app}\banco"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\*"; DestDir: "{app}\dist"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "doc\*"; DestDir: "{app}\doc"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "img\*"; DestDir: "{app}\img"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "src\*"; DestDir: "{app}\src"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "ui\*"; DestDir: "{app}\ui"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Libelula Softwares"; Filename: "{app}\dist\Libelula Softwares.exe"
Name: "{commondesktop}\Libelula Softwares"; Filename: "{app}\dist\Libelula Softwares.exe"

[Run]
Filename: "{app}\dist\Libelula Softwares.exe"; Description: "{cm:LaunchProgram,Libelula Softwares}"; Flags: nowait postinstall skipifsilent
Filename: "{cmd}"; Parameters: "/c pip install -r {app}\requirements.txt"; Flags: runhidden

[Code]
function InitializeSetup(): Boolean;
begin
  // Exemplo de verificação de requisito: Verificar se o .NET Framework 4.5 está instalado
  if not RegKeyExists(HKLM, 'SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full') then
  begin
    MsgBox('O .NET Framework 4.5 ou superior é necessário para instalar este aplicativo.', mbError, MB_OK);
    Result := False;
  end
  else
  begin
    Result := True;
  end;
end;
