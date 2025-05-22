# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

import pytest
import subprocess

from charmed_kubeflow_chisme.rock import CheckRock


@pytest.mark.abort_on_fail
def test_rock():
    """Test that the Feast UI Rock is built correctly and has feast installed."""
    check_rock = CheckRock("rockcraft.yaml")
    rock_image = check_rock.get_name()
    rock_version = check_rock.get_version()
    LOCAL_ROCK_IMAGE = f"{rock_image}:{rock_version}"

    # 1. Check that the feast package is installed
    result = subprocess.run(
        [
            "docker",
            "run",
            "--entrypoint",
            "/bin/bash",
            LOCAL_ROCK_IMAGE,
            "-c",
            "pip list | grep '^feast '"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )

    assert "feast" in result.stdout, "Feast is not installed"

    # 2. Sanity check that the `feast ui --help` command runs successfully
    result_ui = subprocess.run(
        [
            "docker",
            "run",
            "--entrypoint",
            "feast",
            LOCAL_ROCK_IMAGE,
            "ui",
            "--help"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )

    assert "Usage" in result_ui.stdout or "usage" in result_ui.stdout, "Feast UI CLI not functioning as expected"
