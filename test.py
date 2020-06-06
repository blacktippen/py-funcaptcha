from py_funcaptcha import FunCaptchaSession

session = FunCaptchaSession(
    public_key="9F35E182-C93C-EBCC-A31D-CF8ED317B996",
    service_url="https://roblox-api.arkoselabs.com",
    page_url="https://www.roblox.com/Login",
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    proxy="localhost:8866",
    verify=False)
ch = session.create_new_challenge()

print("Challenge ID:", ch.token)
print("Session ID:", ch.session_token)
print("# of images:", len(ch.image_urls))

for image, submit in ch.get_iter():
    image.save("latest.png")
    print(submit(ch.angle))
