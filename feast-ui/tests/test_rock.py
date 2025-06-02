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

    # Sanity check that the `feast ui --help` command runs successfully
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

def test_feast_ui_index_has_correct_manifest_href():
    """Ensure index.html contains href to /feast/manifest.json."""
    check_rock = CheckRock("rockcraft.yaml")
    rock_image = check_rock.get_name()
    rock_version = check_rock.get_version()
    LOCAL_ROCK_IMAGE = f"{rock_image}:{rock_version}"

    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--entrypoint",
            "/bin/bash",
            LOCAL_ROCK_IMAGE,
            "-c",
            'grep -ri "href=\"/feast/manifest.json\"" /usr/local/lib/python3.10/dist-packages/feast/ui/build/index.html && exit 1 || exit 0',
        ],
        check=True,
    )