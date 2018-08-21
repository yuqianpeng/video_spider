from qiniu import Auth
from qiniu import BucketManager

accessKey = 'x'
secretKey = 'x'
bucket  = 'x'
q = Auth(accessKey, secretKey)
bucketa = BucketManager(q)
url = 'http://vm18003.baomihua.com/46d7a10ef91cc89eb147b828ae0a68bc/5B173A26/3780/37790670_7_1c8804982fb6b9b8f60f5d02e9abbbdc.mp4'
key = 'test.mp4'
ret, info = bucketa.fetch(url, bucket, key)
print(info)
assert ret['key'] == key