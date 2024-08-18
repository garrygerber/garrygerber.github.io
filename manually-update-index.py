import yaml
import requests
from datetime import datetime
import base64
import tempfile
import tarfile
import io
import shutil
import os
import hashlib

# GitHub API settings
GITHUB_API_URL = "https://api.github.com"
REPO_OWNER = "garrygerber"
REPO_NAME = "garrygerber.github.io"
GITHUB_TOKEN = ""

def get_github_releases():
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/releases"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def download_and_extract_chart_yaml(asset_url):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/octet-stream"
    }
    response = requests.get(asset_url, headers=headers, allow_redirects=True)
    response.raise_for_status()

    content = response.content
    digest = hashlib.sha256(content).hexdigest()

    with tempfile.TemporaryDirectory() as tmpdirname:
        tgz_path = os.path.join(tmpdirname, 'chart.tgz')
        with open(tgz_path, 'wb') as tgz_file:
            tgz_file.write(content)
        
        with tarfile.open(tgz_path, 'r:gz') as tar:
            chart_yaml_info = next((m for m in tar.getmembers() if m.name.endswith('Chart.yaml')), None)
            if chart_yaml_info:
                chart_yaml_content = tar.extractfile(chart_yaml_info).read().decode('utf-8')
                return yaml.safe_load(chart_yaml_content), digest
    return None, None

def build_index_from_releases(releases):
    index_data = {
        "apiVersion": "v1",
        "generated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "entries": {}
    }

    for release in releases:
        for asset in release['assets']:
            if asset['name'].endswith('.tgz'):
                chart_yaml, digest = download_and_extract_chart_yaml(asset['browser_download_url'])
                if chart_yaml:
                    chart_name = chart_yaml.get('name')
                    version = chart_yaml.get('version')
                    
                    entry = {
                        "apiVersion": chart_yaml.get('apiVersion', 'v2'),
                        "appVersion": chart_yaml.get('appVersion', '1.0.0'),
                        "created": release['created_at'],
                        "description": chart_yaml.get('description', 'No description provided'),
                        "digest": digest,
                        "name": chart_name,
                        "urls": [asset['browser_download_url']],
                        "version": version,
                        "home": chart_yaml.get('home', ''),
                        "sources": chart_yaml.get('sources', []),
                        "keywords": chart_yaml.get('keywords', []),
                        "maintainers": chart_yaml.get('maintainers', []),
                        "type": chart_yaml.get('type', 'application')
                    }

                    if chart_name not in index_data['entries']:
                        index_data['entries'][chart_name] = []
                    index_data['entries'][chart_name].append(entry)

    # Sort versions within each chart
    for chart_entries in index_data['entries'].values():
        chart_entries.sort(key=lambda x: x['created'], reverse=True)

    return index_data

def save_index_yaml(data, file_path='index.yaml'):
    with open(file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)

def main():
    releases = get_github_releases()
    # print("found releases:" + str(releases))
    index_data = build_index_from_releases(releases)
    save_index_yaml(index_data)
    print("index.yaml has been rebuilt successfully from GitHub releases and Chart.yaml files.")

if __name__ == "__main__":
    main()