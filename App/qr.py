import qrcode

employee_id = "84504903"
base_url = "https://spread-chelsea-find-lying.trycloudflare.com"  
full_url = f"{base_url}/scan?id={employee_id}"

qr = qrcode.make(full_url)
qr.save(f"{employee_id}_qr.png")
print(f"QR code generated for: {full_url}")
