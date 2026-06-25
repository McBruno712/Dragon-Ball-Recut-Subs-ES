from dbsubs_lat.cli import build_parser


def test_build_parser_supports_batch():
    p = build_parser()
    args = p.parse_args(["--videos-dir", "/tmp", "--batch", "E02-E21"])
    assert args.batch == "E02-E21"
    assert args.pilot is None


def test_build_parser_supports_pilot_still():
    p = build_parser()
    args = p.parse_args(["--videos-dir", "/tmp", "--pilot", "E05"])
    assert args.pilot == "E05"
    assert args.batch is None
