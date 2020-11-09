import pytest
import subprocess
import testinfra


# scope='session' uses the same container for all the tests;
# scope='function' uses a new container per test function.
@pytest.fixture(scope='session')
def host(request):
    # build local ./Dockerfile
    subprocess.check_call(['docker', 'build', '-t', 'testinfra-nginx', '.'])
    # run a container
    docker_id = subprocess.check_output(
        ['docker', 'run', '-d', '--name', 'testinfra-nginx', 'testinfra-nginx']).decode().strip()
    # return a testinfra connection to the container
    yield testinfra.get_host("docker://" + docker_id)
    # at the end of the test suite, destroy the container
    subprocess.check_call(['docker', 'rm', '-f', docker_id])


def test_package(host):
    # 'host' now binds to the container
    assert host.package("nginx").is_installed
    assert host.package("nginx").version == "1.19.4-1~buster"

def test_binary(host):
    assert host.file("/usr/sbin/nginx").mode == 0o755

def test_service(host):
    assert host.service("nginx").is_running

def test_bin_version(host):
    cmd = host.run("nginx -v")
    assert cmd.stderr == "nginx version: nginx/1.19.4"

def test_file_content(host):
    assert host.file("/usr/share/nginx/html/index.html").contains("This is a Heading")
