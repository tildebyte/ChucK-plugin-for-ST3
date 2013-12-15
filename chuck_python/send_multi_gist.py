import json
from urllib.request import urlopen
import webbrowser
import time 

def upload(gist_files_dict, project_name, public_switch):
  
    pf = time.strftime("_%Y_%m_%d_%H-%M")
    gist_post_data = {  'description': project_name+pf, 
                        'public': public_switch,
                        'files': gist_files_dict
                    }
 
    json_post_data = json.dumps(gist_post_data).encode('utf-8')
 
    def get_gist_url(found_json):
        wfile = json.JSONDecoder()
        wjson = wfile.decode(found_json)
        gist_url = 'https://gist.github.com/' + wjson['id']
 
        print(gist_url)
        webbrowser.open(gist_url)
        # or just copy url to clipboard?
 
    def upload_gist():
        print('sending')
        url = 'https://api.github.com/gists'
        json_to_parse = urlopen(url, data=json_post_data)
        
        print('received response from server')
        found_json = json_to_parse.readall().decode()
        get_gist_url(found_json)
 
    upload_gist()
 
