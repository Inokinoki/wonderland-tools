import json
import urllib.request

base_url = "http://www.wangjiuyue.cn/"

file_name = "dict.json"

if __name__ == "__main__":
    with open(file_name, "r", encoding='utf-8') as f_desc:
        i = 1
        mapping_obj = json.load(f_desc)
        for obj in mapping_obj:
            for o in obj:
                print(o)
                if "url" in o.keys() and len(o["url"]) > 0:
                    urllib.request.urlretrieve(base_url + o["url"], "htmls/{}.".format(i) + o["name"] + ".html")
            i += 1
