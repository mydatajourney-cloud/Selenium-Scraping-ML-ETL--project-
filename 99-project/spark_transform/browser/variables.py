
sourceTypeDict = {
    "google": "search",
    "bing": "search",
    "yahoo": "search",
    "baidu": "search",
    "duckduckgo": "search",
    "ask": "search",
    "aol": "search",
    "yandex": "search",
    "naver": "search",
    "ecosia": "search",
    "seznam": "search",

    "facebook": "social media",
    "instagram": "social media",
    "twitter": "social media",  # or "x" if you're using the new name
    "linkedin": "social media",
    "pinterest": "social media",
    "tiktok": "social media",
    "snapchat": "social media",
    "reddit": "social media",
    "wechat": "social media",
    "tumblr": "social media",
    "vk": "social media",
    "line": "social media",
    "threads": "social media",

    "glamira": "company webpage",

    #  Direct (no referrer)
    "(direct)": "direct",  # use this key if your logic adds it when referrer is missing
    "": "direct",          # for empty referrer values
    None: "direct"         # handle None values explicitly
}