from pyngrok import ngrok
import os

ngrok.set_auth_token("3Dm16CV7G16tYqzrM9jsVuTlSpy_4E4wVucz1LxqmB4yt3jg")

# شغّل Streamlit
os.system("streamlit run app.py &")


# افتح رابط عام
public_url = ngrok.connect(8501)

print("🌍 الرابط حقك:")
print(public_url)

input("اضغط Enter للإغلاق...")
