import secrets

# gen nginx conf
with open('/etc/nginx/nginx.conf') as f:
    conf = f.read()

secure_passwd = secrets.token_hex(16)
with open('./.secure_password', 'w') as f:
    f.write(secure_passwd)

url_prefix = '/share/'
new_conf = conf.replace('\t# Gzip Settings', '\t# Gzip Settings\n\tcharset utf-8,gbk;\n\tserver {\n\t\tlisten\t8080 default_server;\n\t\tlocation ' + url_prefix + ' {\n\t\t\talias /mnt/media/;\n\t\t\tadd_header Cache-Control max-age=31536000;\n\t\t\tsecure_link $arg_md5,$arg_expires;\n\t\t\tsecure_link_md5  "$secure_link_expires$uri ' +
                        secure_passwd + '";\n\t\t\tif ($secure_link = "") {\n\t\t\t\treturn 404;\n\t\t\t}\n\t\t\tif ($secure_link = "0") {\n\t\t\t\treturn 403;\n\t\t\t}\n\t\t}\n\t\tlocation / {\n\t\t\tproxy_pass http://127.0.0.1:5006;\n\t\t}\n\t}\n\t')

with open('/etc/nginx/nginx.conf', 'w') as f:
    f.write(new_conf)

# gen jwt secret key
secret_key = secrets.token_hex(20)
with open('./.secret', 'w') as f:
    f.write(secret_key)
