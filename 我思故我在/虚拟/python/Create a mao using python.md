`import folium`
`from IPython.display import display`
`map_center = [40.7128,-74.0060]`
`mymap = folium.Map(location=map_center,zoom_start=12)folium.Marker(`
	`[40.7128,-74.0060],`
	 `popup="New York,`
	 `icon = folium.Icon(color="blue", icon="info-sign").add_to(mymap)"`
`display(mymap)`
##### Generate a WIFI QR code using python
`pin install wifi-qrcode-generator`
`from wifi_qrcode_generator import wifi_qrcode`
`qr_code = wifi_qrcode("clcoding",hidden=False,authentication_type="WPA",password="123445uii")`
`qr_code_img = qr_code.make_image()`
`qr_code_img.save("wifi_qr_code.png")`
##### Password Authentication using python
`import getpass`
`database = {"clcoding": "79802","pythoncoding": "234"}`
`username = input("Enter Your Username")`
`password = getpass.getpass("Enter Your Password: ")`
`for i in database.keys():`
	`if username == i :`
		`while password ！= database.get(i):`
			 `password = getpass.getpass("Enter Your Password Again: ")`
			`break`
`print("Verified")`
		
