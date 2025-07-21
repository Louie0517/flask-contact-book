import qrcode

url = "http://192.168.1.10:5000/scan?id=83450132"
img = qrcode.make(url)
img.save("employee_qr.png")
