print "====Before_Build===="
Import("env")
import gzip
import shutil
import os
import subprocess
from platformio import util 
import pip


def install_package(package):
    subprocess.call(["pip","install","--upgrade",package])

install_package("html_utils_becothal")
from html_utils import HTML

def before_uploadfs():
    print "----uploadfs----"
    config = util.load_project_config()
    if config.get("env:esp8285","web_ui_path") == "": 
        print "web_ui_path is not set"
        return
    inlinedWebUI = config.get("env:esp8285","web_ui_path")[:config.get("env:esp8285","web_ui_path").find(".html")] + "_inlined.html"
    spiff_dir = config.get("env:esp8285","spiff_dir")
    html_file = HTML()
    html_file.readFile(config.get("env:esp8285","web_ui_path"))
    html_file.inlineCSS()
    html_file.inlineJS()
    html_file.writeFile(inlinedWebUI)
    if not os.path.exists(spiff_dir):
        os.mkdir(spiff_dir)
    with open(inlinedWebUI) as f_in, gzip.open(spiff_dir + "index.html.gz","wb") as f_out:
        shutil.copyfileobj(f_in,f_out) 
    os.remove(inlinedWebUI)

print "Current build targets", map(str, BUILD_TARGETS) 
if("uploadfs" in BUILD_TARGETS or "buildfs" in BUILD_TARGETS):
    before_uploadfs()
else: 
    print "No extraScript for this Target"



#env.AddPreAction("uploadfs",before_buildfs)
