# Các biện pháp phòng chống

- Các biện pháp chống brute force thường không bảo vệ hoàn toàn nếu dùng đơn lẻ, cần kết hợp với nhau theo mô hình defense-in-depth thì đạt mức bảo vệ hợp lý

## 1. Rate limit

- Là giới hạn tốc độ gửi request đăng nhập

```php
Một IP chỉ được thử 5 lần / phút
Một tài khoản chỉ được thử 10 lần / 10 phút
Một thiết bị chỉ được thử 20 lần / giờ
```

- NIST hiện cũng yêu cầu verifier phải có cơ chế rate limiting để giới hạn số lần xác thực thất bại trên tài khoản người dùng
- Tuy nhiên rate limit theo IP không đủ nếu attacker dùng nhiều IP, proxy, botnet,..

## 2. Accout lockout

- Là khóa tài khoản sau nhiều lần đăng nhập sai

```php
Sai mật khẩu 5 lần trong 10 phút
→ khóa đăng nhập tài khoản 15 phút
```

- Tuy nhiên, kẻ tấn công vẫn có thể gây ra tấn công DDoS, kẻ tấn công cố tình nhập sai để làm cho chủ tài khoản thực sự không thể đăng nhập
- Cần tích hợp thêm 1 vài giải pháp để khi người dùng thực sự quay lại thì có thể đăng nhập lại được luôn

## 3. MFA - Multi-Factor Authentication

- Là yêu cầu người dùng xác thực từ 2 loại yếu tố trở lên

```php
Password + mã OTP
Password + FIDO2
Password + passkey
```

- OWASP đánh giá MFA là một trong những biện pháp mạnh nhất để chống các cuộc tấn công liên quan đến mật khẩu, bao gồm brute force, credential stuffing và password spraying.
- MFA làm cho việc biết mật khẩu chưa đủ để đăng nhập
- MFA là khi người dùng phải đưa ra hơn 1 loại bằng chứng để xác thực vào hệ thống. Các yếu tố thường gặp nhất trong web là:
  - Something you know: Mật khẩu, mã PIN
  - Something you have: Điện thoại nhận OTP, App google, …
  - Something you are: Vân tay, khuôn mặt, mống mắt, giọng nói,…

### SMS OTP

- Là mã dùng 1 lần được gửi qua tin nhắn điện thoại

```php
Bạn đăng nhập bằng mật khẩu
→ hệ thống gửi mã 6 số qua SMS
→ bạn nhập mã đó
→ hệ thống cho đăng nhập
```

- Ví dụ attacker có thể lừa người dùng nhập mã SMS vào trang giả mạo

```php
Trang giả giống thật
→ user nhập username/password
→ user nhập luôn mã SMS OTP
→ attacker dùng thông tin đó đăng nhập thật
```

### WebAuthn là gì?

- **WebAuthn là API để website/app yêu cầu trình duyệt hoặc thiết bị xác thực người dùng bằng public key cryptography**, thay vì chỉ dựa vào mật khẩu.
- Bản chất có nhiệm vụ xác minh người dùng bằng việc yêu cầu người dùng ký 1 challange được gửi từ server, nếu server có thể dùng khóa công khai giải mã được thì cặp private - public key đã đúng
- Nó là cơ chế giúp sử dụng passkey để xác thực thay vì dùng mật khẩu

### Passkey là gì?

- Là 1 loại thông tin đăng nhập hiện đại dùng để thay thế mật khẩu, nhưng nó không phải là 1 chuỗi ký tự như

```php
123456
admin@123
Password@2024
```

- Mà bản chất là 1 cặp khóa bất đối xứng

```php
Public key  +  Private key
```

- Luồng hoạt động khi sử dụng passkey

```php
1. Website/app yêu cầu tạo passkey
2. Website gọi WebAuthn trên trình duyệt,nhận đầu vào là 1 gói dữ liệu PublicKeyCredentialCreationOptions từ server tạo ra. Trình duyệt kiểm tra trường rp.id trong gói tin có khớp với domain đang yêu cầu tạo passkey không
3. Sau khi kiểm tra xong, trình duyệt gọi xuống authenticator có thể là: Chip bảo mật, Face ID, Touch ID, Window Hello,...
4. Authenticator tạo ra 1 public key credential source gắn với authenticator và trả về public key tương ứng với private key. Nó giữ lại private key và gửi lại, còn public key được gửi lại cho WebAuthn dưới dạng 1 object PublicKeyCredential
5. Thiết bị yêu cầu Face ID / vân tay / PIN để bảo vệ private key
```

- Khi đó, server không lưu mật khẩu dưới dạng hash như bình thường nữa mà lưu dưới dạng

```php
User: dao@example.com

Passkey 1: trên iPhone
credential_id = A1B2C3
public_key = PK_iphone

Passkey 2: trên laptop Windows
credential_id = X9Y8Z7
public_key = PK_windows
```

⇒ Bản chất thì WebAuthn chính là “người vận chuyển”. Còn passkey chính là chiếc chìa khóa cần được vận chuyển. Vấn đề là chiếc chìa khóa này phải mở từ xa, nên cần phải xác thực xem có đúng ổ đúng chìa không trước khi mở.
