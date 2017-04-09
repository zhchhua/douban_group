from fetch_free_proxyes import fetch_all


ip_list = fetch_all()

i=0
for ip in ip_list:
    print(ip)
    i=i + 1

print("有效代理数目为：%d"%i)
