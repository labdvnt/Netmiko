# Netmiko


## 🔧 Multi-Device Network Command Automation with Netmiko

This Python script automates the process of connecting to multiple network devices (Cisco IOS, NX-OS, XR, etc.) via SSH using Netmiko, and sends predefined commands from a JSON file. The results are saved in a timestamped report file with structured JSON-like output using TextFSM.

### Features

- Reads devices and commands from external JSON files.
- Connects to multiple devices using SSH (Netmiko).
- Enables privileged EXEC mode on IOS/XE devices.
- Sends platform-specific commands.
- Parses command output using TextFSM (structured data).
- Saves results to a timestamped `.txt` file (`TumRapor_YYYYMMDD_HHMMSS.txt`).

### Input Files

- `devices.json`: Contains IP, port, username, password, model_type, and device_type for each device.
- `commands.json`: Contains a list of commands for each model_type.

---

## 🔧 Netmiko ile Çoklu Cihaza Otomatik Komut Gönderimi

Bu Python betiği, Netmiko kütüphanesini kullanarak SSH üzerinden birden fazla ağ cihazına (Cisco IOS, NX-OS, XR vb.) bağlanır, cihaz türüne uygun komutları gönderir ve sonuçları zaman damgalı bir dosyada saklar. TextFSM desteği sayesinde çıktılar düzenli (yapılandırılmış) şekilde kaydedilir.

### Özellikler

- Cihaz ve komut listesi dış JSON dosyalarından okunur.
- SSH ile çoklu cihaza bağlantı sağlar.
- IOS/XE cihazlarda enable modu aktif eder.
- Cihaz modeline uygun komutlar çalıştırılır.
- Komut çıktıları TextFSM ile yapılandırılır.
- Çıktılar zaman damgalı `.txt` dosyasına yazılır (`TumRapor_YYYYMMDD_HHMMSS.txt`).

### Giriş Dosyaları

- `devices.json`: Her cihaz için IP, port, kullanıcı adı, şifre, model_type ve device_type içerir.
- `commands.json`: Her model_type için gönderilecek komutları listeler.
