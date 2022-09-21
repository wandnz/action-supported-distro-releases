#!/usr/bin/env python3

import argparse
import csv
import datetime
import json
import os


def parse_date(date):
    if not date:
        return None
    return datetime.datetime.fromisoformat(date).date()


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--distros', required=True)
    argparser.add_argument('--include-lts', action='store_true')
    argparser.add_argument('--include-extended-lts', action='store_true')
    argparser.add_argument('--distro-info-data-dir', required=True)

    args = argparser.parse_args()

    today = datetime.date.today()

    supported_distro_releases = []

    print(f"today is {today}")

    for distro in args.distros.split(','):
        distro_csv = os.path.join(args.distro_info_data_dir, distro) + '.csv'
        with open(distro_csv, encoding='utf8') as did_csv_file:
            distro_releases = csv.DictReader(did_csv_file, delimiter=',')
            for distro_release in distro_releases:
                distro_release_series = distro_release['series']
                distro_start_date = parse_date(distro_release['release'])
                distro_end_date = parse_date(distro_release['eol'])

                if not distro_start_date:
                    print(f"{distro} {distro_release['series']} is unreleased")
                    continue

                lts_dict_key = None

                if args.include_lts:
                    if distro == 'debian':
                        lts_dict_key = 'eol-lts'

                if args.include_extended_lts:
                    if distro == 'debian':
                        lts_dict_key = 'eol-elts'
                    elif distro == 'ubuntu':
                        lts_dict_key = 'eol-esm'

                if lts_dict_key and distro_release[lts_dict_key]:
                    distro_end_date = parse_date(distro_release[lts_dict_key])

                if distro_start_date <= today <= distro_end_date:
                    print(f"{distro} {distro_release['series']} is supported")
                    supported_distro_releases.append(f"{distro}:{distro_release_series}")
                else:
                    print(f"{distro} {distro_release['series']} is not supported, "
                          f"support start date = {distro_start_date}, "
                          f"support end date = {distro_end_date}")

    matrix = json.dumps(supported_distro_releases)
    print(f"::set-output name=matrix::{matrix}")


if __name__ == "__main__":
    main()
