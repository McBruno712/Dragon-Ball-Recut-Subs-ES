from dbsubs_lat.styles import rewrite_styles


def test_rewrite_styles_replaces_avenir_black_with_arial():
    styles = [
        "Default,Avenir Black,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1",
        "Dragon Ball,Avenir Black,35,&H00FFFFFF,&H0000FFFF,&H00000000,&H00000000,0,0,0,0,100,100,0.5,0,1,2,0.4,2,20,20,25,1",
    ]
    out = rewrite_styles(styles)
    assert "Avenir Black" not in "\n".join(out)
    assert "\n".join(out).count("Arial") == 2


def test_rewrite_styles_keeps_other_fonts():
    styles = [
        "Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1",
    ]
    out = rewrite_styles(styles)
    assert out[0].startswith("Default,Arial,20,")
