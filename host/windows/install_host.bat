:: Copyright 2014 The Chromium Authors. All rights reserved.
:: Use of this source code is governed by a BSD-style license that can be
:: found in the LICENSE file.

:: Change HKCU to HKLM if you want to install globally.
:: %~dp0 is the directory containing this bat script and ends with a backslash.
REG ADD "HKCU\Software\Google\Chrome\NativeMessagingHosts\br.com.bluefocus.printhost" /ve /t REG_SZ /d "%~dp0br.com.bluefocus.printhost-win.json" /f
REG ADD "HKCU\Software\Google\Chrome\NativeMessagingHosts\br.com.bluefocus.printlist" /ve /t REG_SZ /d "%~dp0br.com.bluefocus.printlist-win.json" /f

REG ADD "HKLM\Software\Google\Chrome\NativeMessagingHosts\br.com.bluefocus.printhost" /ve /t REG_SZ /d "%~dp0br.com.bluefocus.printhost-win.json" /f
REG ADD "HKLM\Software\Google\Chrome\NativeMessagingHosts\br.com.bluefocus.printlist" /ve /t REG_SZ /d "%~dp0br.com.bluefocus.printlist-win.json" /f


REG ADD "HKLM\Software\Policies\Chromium\ExtensionInstallForcelist\1" /ve /t REG_SZ /d "mnndbokmnjpaieoghbkcdohflohhnhkn;https://clients2.google.com/service/update2/crx"