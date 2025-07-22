import qrcode

employee_id = "53554630"
base_url = " https://insights-bald-marble-chances.trycloudflare.com"  # your actual tunnel URL
full_url = f"{base_url}/scan?id={employee_id}"

qr = qrcode.make(full_url)
qr.save(f"{employee_id}_qr.png")
print(f"QR code generated for: {full_url}")
