-- Table for tweets
CREATE TABLE IF NOT EXISTS twitter_data (
    id TEXT PRIMARY KEY,
    text TEXT,
    created_at TEXT,
    author_id TEXT,
    lang TEXT
);

-- Table for Reddit posts
CREATE TABLE IF NOT EXISTS reddit_data (
    id TEXT PRIMARY KEY,
    title TEXT,
    content TEXT,
    subreddit TEXT,
    timestamp TEXT,
    author TEXT
);