$cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "test" -CertStoreLocation "Cert:\CurrentUser\My"
$certPath = Join-Path -Path $PSScriptRoot -ChildPath "test.pfx"
$certPassword = ConvertTo-SecureString -String "963852" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath $certPath -Password $certPassword
Write-Host "PFX certificate generated at: $certPath"