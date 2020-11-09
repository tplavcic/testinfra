"""Role testing files using testinfra."""

def test_hosts_file(host):
    f = host.file("/etc/hosts")
    assert f.exists
    assert f.user == "root"
    assert f.group == "root"

def test_custom_directory(host):
    f = host.file("/var/lib/user")
    assert f.exists
    assert f.user == "root"
    assert f.group == "root"

def check_devops_directory(host):
    f = host.file("/tmp/devops_directory")
    assert f.exists

def test_nginx_is_installed(host):
    nginx = host.package("nginx")
    assert nginx.is_installed

def test_nginx_running_and_enabled(host):
    nginx = host.service("nginx")
    assert nginx.is_running
    assert nginx.is_enabled

def test_nginx_config(host):
    assert host.file("/etc/nginx/nginx.conf").contains("user nginx;")

def test_config_permissions(host):
    assert oct(host.file('/etc/nginx/nginx.conf').mode) == '0o644'

def test_index_content(host):
    page = host.file("/usr/share/nginx/html/index.html")
    assert page.contains("Page Title")
