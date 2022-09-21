#!/bin/bash

set -euo pipefail

distros=${DISTROS:-"debian,ubuntu"}
include_lts=${INCLUDE_LTS:-"true"}
include_extended_lts=${INCLUDE_EXTENDED_LTS:-"false"}

git_tmp_dir=$(mktemp -d /tmp/distro-info-data-XXXXX)
git clone --depth 1 https://salsa.debian.org/debian/distro-info-data "${git_tmp_dir}"

additional_args=()

if [ "${include_lts}" == "true" ]; then
    additional_args+=("--include-lts")
fi

if [ "${include_extended_lts}" == "true" ]; then
    additional_args+=("--include-extended-lts")
fi

"${GITHUB_ACTION_PATH}"/parse_distro-info-data.py --distro-info-data-dir "${git_tmp_dir}" --distros "${distros}" "${additional_args[@]}"

rm -rf "${git_tmp_dir}"
