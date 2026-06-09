"""
Instagram Graph API module.

Required environment variables:
    INSTAGRAM_ACCESS_TOKEN  — long-lived Page Access Token
    INSTAGRAM_USER_ID       — numeric Instagram Business Account ID

Both are obtained from Meta for Developers (developers.facebook.com).
See README or docs for the exact step-by-step setup.
"""

import os
import requests
import streamlit as st

_BASE = "https://graph.facebook.com/v20.0"
_TIMEOUT = 10


def _configured() -> bool:
    return bool(os.getenv("INSTAGRAM_ACCESS_TOKEN")) and bool(os.getenv("INSTAGRAM_USER_ID"))


def _get(path: str, params: dict) -> dict:
    params["access_token"] = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
    resp = requests.get(f"{_BASE}/{path}", params=params, timeout=_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_profile() -> dict | None:
    """Followers, following, post count, username."""
    if not _configured():
        return None
    uid = os.getenv("INSTAGRAM_USER_ID")
    return _get(uid, {"fields": "followers_count,follows_count,media_count,username"})


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_insights() -> dict | None:
    """Weekly reach, impressions, profile views (past 7 days)."""
    if not _configured():
        return None
    uid = os.getenv("INSTAGRAM_USER_ID")
    raw = _get(
        f"{uid}/insights",
        {"metric": "reach,impressions,profile_views", "period": "week"},
    )
    result = {}
    for item in raw.get("data", []):
        values = item.get("values", [])
        if values:
            # take the most recent period value
            result[item["name"]] = values[-1]["value"]
    return result


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_engagement_rate() -> float | None:
    """Average engagement rate across last 12 posts (%)."""
    if not _configured():
        return None
    uid = os.getenv("INSTAGRAM_USER_ID")
    profile = fetch_profile()
    if not profile or not profile.get("followers_count"):
        return None
    followers = profile["followers_count"]
    media = _get(
        f"{uid}/media",
        {"fields": "like_count,comments_count", "limit": 12},
    )
    posts = media.get("data", [])
    if not posts:
        return None
    total = sum(p.get("like_count", 0) + p.get("comments_count", 0) for p in posts)
    return round((total / len(posts)) / followers * 100, 2)


def get_all() -> dict:
    """
    Returns a single dict of display-ready values.
    Falls back to None for each metric if the API is not connected or errors.
    """
    try:
        profile  = fetch_profile()
        insights = fetch_insights()
        eng_rate = fetch_engagement_rate()
    except requests.RequestException:
        return {k: None for k in [
            "followers", "following", "posts",
            "reach_week", "impressions_week",
            "engagement_rate", "profile_visits",
        ]}

    if profile is None:
        return {k: None for k in [
            "followers", "following", "posts",
            "reach_week", "impressions_week",
            "engagement_rate", "profile_visits",
        ]}

    ins = insights or {}
    return {
        "followers":        profile.get("followers_count"),
        "following":        profile.get("follows_count"),
        "posts":            profile.get("media_count"),
        "reach_week":       ins.get("reach"),
        "impressions_week": ins.get("impressions"),
        "engagement_rate":  eng_rate,
        "profile_visits":   ins.get("profile_views"),
    }


def is_connected() -> bool:
    return _configured()
