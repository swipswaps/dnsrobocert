import subprocess
import sys
from distutils.version import StrictVersion


def main():
    git_clean = subprocess.check_output("git status --porcelain", universal_newlines=True).strip()
    # if git_clean:
    #     raise RuntimeError("Error, git workspace is not clean: \n{0}".format(git_clean))

    current_version = subprocess.check_output(
        "poetry version", shell=True, universal_newlines=True
    ).replace("dnsrobocert ", "")
    current_version = StrictVersion(current_version)

    print("Current version is: {0}".format(current_version))
    print("Please insert new version:")
    new_version = str(input())

    new_version = StrictVersion(new_version)

    if new_version <= current_version:
        raise RuntimeError(
            "Error new version is below current version: {0} < {1}".format(
                new_version, current_version
            )
        )

    try:
        subprocess.check_call("poetry version {0}".format(new_version), shell=True)
        subprocess.check_call("poetry run isort src test utils", shell=True)
        subprocess.check_call("poetry run black src test utils", shell=True)
        subprocess.check_call("poetry run mypy src", shell=True)
        subprocess.check_call("poetry run pytest test", shell=True)
    except subprocess.CalledProcessError:
        subprocess.check_call("git reset --hard")


if __name__ == "__main__":
    main()