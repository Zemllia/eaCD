import hashlib
import hmac

from flask import Flask, request
import json
import os
import subprocess


app = Flask(__name__)


@app.route('/new-commit', methods=['POST'])
def hello():
    request_data = request.get_json()
    print("Catched update!")

    with open('config.json') as json_file:
        data = json.load(json_file)
    for repository in data['repositories']:
        if request_data.get("repository").get("name") == repository.get("name") and \
                (request_data.get("ref") == f"refs/heads/{repository.get('branch')}" or request_data.get("before") == '0000000000000000000000000000000000000000'):
            if not _validate_signature(request.headers, request.data, repository.get('webhook_secret')):
                return 'ok'
            if data.get("OSType") == 'L':
                os.system("sh " + ("/" if repository.get("location")[0] != "/" else "") + repository.get("location")
                          + "/EaCi/deploy.sh")
            elif data.get("OSType") == 'W':
                print(r"" + repository.get("location") + r"/EaCi/")
                subprocess.call([r"" + repository.get("location") + r"\\EaCi\\deploy.bat"])
    print("Update finished!")

    return 'ok'


def _validate_signature(headers, request_data, secret):
    signature = headers.get("X-Hub-Signature")
    if not signature or not signature.startswith("sha1="):
        return False

    # Create our own signature
    digest = hmac.new(secret.encode(), request_data, hashlib.sha1).hexdigest()

    # Verify signature
    if not hmac.compare_digest(signature, "sha1=" + digest):
        return False
    return True


def start():
    with open('config.json') as json_file:
        data = json.load(json_file)
    for repository in data.get("repositories"):
        check_project_dir = os.path.isdir(repository.get("location"))
        if not check_project_dir:
            raise FileNotFoundError("Cant find project dir for project " + repository.get("name") + " at path "
                                    + repository.get("location"))
        check_git_dir = os.path.isdir(repository.get("location") + "/.git")
        if not check_git_dir:
            raise FileNotFoundError("Cant find git dir for project " + repository.get("name") + " at path "
                                    + repository.get("location"))
        check_eaci_dir = os.path.isdir(repository.get("location") + "/EaCi")
        if not check_eaci_dir:
            os.mkdir(repository.get("location") + "/EaCi")
        check_eaci_sh = os.path.isfile(repository.get("location") + "/EaCi/deploy.sh")
        if not check_eaci_sh:
            f = open(repository.get("location") + "/EaCi/deploy.sh", "a")
            f.write("#!/bin/bash\ncd " + repository.get("location") + "\ngit pull")
            f.close()

        check_eaci_bat = os.path.isfile(repository.get("location") + "/EaCi/deploy.bat")
        if not check_eaci_bat:
            f = open(repository.get("location") + "/EaCi/deploy.bat", "a")
            f.write("cd " + repository.get("location") + "\ngit pull")
            f.close()
    app.run(data.get("host"), data.get("port"), debug=True)


if __name__ == '__main__':
    start()
