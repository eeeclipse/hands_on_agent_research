import pytest

from profiles import load_profile


def test_load_known_profiles():
    phd = load_profile("phd")
    industry = load_profile("industry")

    assert phd.PROFILE_NAME == "PhD Research"
    assert industry.PROFILE_NAME == "Industry Practice"
    assert phd.TEAM_RESEARCH_TOPICS
    assert industry.BLOG_FEEDS


def test_load_unknown_profile_raises_clear_error():
    with pytest.raises(ValueError, match="알 수 없는 프로필"):
        load_profile("career")
