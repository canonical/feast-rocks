# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

import pytest
import subprocess

from charmed_kubeflow_chisme.rock import CheckRock


@pytest.mark.abort_on_fail
def test_rock():
    """Test rock."""
    check_rock = CheckRock("rockcraft.yaml")
    rock_image = check_rock.get_name()
    rock_version = check_rock.get_version()
    LOCAL_ROCK_IMAGE = f"{rock_image}:{rock_version}"

    # Check python executable points to python3
    result = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            LOCAL_ROCK_IMAGE,
            "exec",
            "ls",
            "-l",
            "/usr/bin/python",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    output = result.stdout.strip()
    assert "python3" in output, "/usr/bin/python is NOT pointing to python3"

    # Check app.py exists in root dir
    subprocess.run(
        ["docker", "run", "--rm", LOCAL_ROCK_IMAGE, "exec", "ls", "-la", "/app.py"],
        check=True,
    )
