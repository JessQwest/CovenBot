import configparser

global mod_list
global regions, subregions
global config
global archived_list_url, archive_md

def init():
    global mod_list, regions, subregions, config, archived_list_url, archive_md
    mod_list = []
    regions = []
    subregions = {}

    config = configparser.ConfigParser()
    config.read('config/config.ini')

    archived_list_url = config.get('Wiki', 'archived_list_url')
    archive_md = f"For more listings, see the [archived listings]({archived_list_url})."
