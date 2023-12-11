import rsa

# generate public and private keys with
# rsa.newkeys method,this method accepts
# key length as its parameter
# key length should be atleast 16
publicKey, privateKey = rsa.newkeys(2048)

with open("public.pem", mode="wb") as public:
    public.write(publicKey.save_pkcs1())

with open("private.pem", mode="wb") as private:
    private.write(privateKey.save_pkcs1())
