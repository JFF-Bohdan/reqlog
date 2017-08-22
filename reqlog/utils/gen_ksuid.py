import argparse

import ksuid


def get_gen_ksuid_commandline():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--base62",
        action="store_true",
        help="write output encoded as base62"
    )

    return parser.parse_args()


def main():
    uid = ksuid.ksuid()

    args = get_gen_ksuid_commandline()
    if args.base62:
        print(uid.toBase62())
    else:
        print(str(uid))


if __name__ == "__main__":
    main()
