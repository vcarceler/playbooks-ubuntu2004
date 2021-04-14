#
# vpn-add-hosts.py
#
# Abre el fichero hosts-users.csv y para cada registro
# genera los ficheros username.yml e address.yml.
#
# El fichero hosts-users.csv tiene el siguiente formato:
#
# address,mask,privatekey,userpath,username,usercomment,password
# 10.0.0.160,/20,aabbcc,users/alumnes,usuario1,usuario1 usuario1,secreto1
# 10.0.0.161,/20,bbccaa,users/alumnes,usuario2,usuario2 usuario2,secreto2
# 10.0.0.162,/20,ccaabb,users/alumnes,usuario3,usuario3 usuario3,secreto3
#
#
#
from jinja2 import Template
from rich import print

import crypt
import csv
import os

with open('hosts-users.csv', newline='') as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
        print(row)

        # Generamos el fichero de usuario
        userTemplate = """---
# Alta de usuarios (mkpasswd --method=sha-512)
- name: Usuario {{ username }}
  action: user name={{ username }} {% raw %}groups={{ grupos }}{% endraw %} comment="{{ usercomment }}" append=yes shell=/bin/bash password={{ password }}"""
        template = Template(userTemplate)
        password_hash = crypt.crypt(row["password"])
        f = open(os.path.join(row["userpath"],row["username"] + ".yml"), "w")
        f.write(template.render(username=row["username"], usercomment=row["usercomment"], password=password_hash))
        f.close()
        print("Generado usuario: " + row["username"])

        # Generamos el fichero del host en la vpn
        hostTemplate = """
- name: Prepara /etc/wireguard/wg0.conf
  vars:
          privatekey: {{ privatekey }}
          address: {{ address }}{{ mask }}
  template:
    src: templates/vpn-control.j2
    dest: /etc/wireguard/wg0.conf
    owner: root
    group: root
    mode: 0400

- include: "{{ userfile }}"

"""
        template = Template(hostTemplate)
        f = open(os.path.join("vpn", row["address"] + ".yml"), "w")
        f.write(template.render(privatekey=row["privatekey"], address=row["address"], mask=row["mask"], userfile=os.path.join(row["userpath"],row["username"] + ".yml")))
        f.close()
        print("Generado host: "  + row["address"])
