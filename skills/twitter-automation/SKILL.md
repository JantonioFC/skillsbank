---
name: twitter-automation
description: |-
  Automate Twitter/X tasks via Rube MCP (Composio): posts, search, users, bookmarks, lists, media. Always search tools first for current schemas.
risk: safe
source: community
date_added: '2026-02-27'
license: MIT
---
# Twitter/X Automation

## When to Use

Use this skill as needed to perform the specified automation task.

Automate Twitter/X via [inference.sh](https://inference.sh) CLI.

![Twitter/X Automation](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kgad3pxsh3z3hnfpjyjpx4x4.jpeg)

## Quick Start

```bash
# Install CLI
curl -fsSL https://cli.inference.sh | sh && infsh login

# Post a tweet
infsh app run x/post-tweet --input '{"text": "Hello from inference.sh!"}'
```

## Available Apps

| App | App ID | Description |
|-----|--------|-------------|
| Post Tweet | `x/post-tweet` | Post text tweets |
| Create Post | `x/post-create` | Post with media |
| Like Post | `x/post-like` | Like a tweet |
| Retweet | `x/post-retweet` | Retweet a post |
| Delete Post | `x/post-delete` | Delete a tweet |
| Get Post | `x/post-get` | Get tweet by ID |
| Send DM | `x/dm-send` | Send direct message |
| Follow User | `x/user-follow` | Follow a user |
| Get User | `x/user-get` | Get user profile |

## Examples

### Post a Tweet

```bash
infsh app run x/post-tweet --input '{"text": "Just shipped a new feature! 🚀"}'
```

| Task | Tool Slug | Key Params |
|------|-----------|------------|
| Create post | TWITTER_CREATION_OF_A_POST | text |
| Delete post | TWITTER_POST_DELETE_BY_POST_ID | id |
| Look up post | TWITTER_POST_LOOKUP_BY_POST_ID | id |
| Recent search | TWITTER_RECENT_SEARCH | query |
| Archive search | TWITTER_FULL_ARCHIVE_SEARCH | query |
| Search counts | TWITTER_RECENT_SEARCH_COUNTS | query |
| My profile | TWITTER_USER_LOOKUP_ME | (none) |
| User by name | TWITTER_USER_LOOKUP_BY_USERNAME | username |
| User by ID | TWITTER_USER_LOOKUP_BY_ID | id |
| Users by IDs | TWITTER_USER_LOOKUP_BY_IDS | ids |
| Upload media | TWITTER_UPLOAD_MEDIA | media |
| Upload video | TWITTER_UPLOAD_LARGE_MEDIA | media |
| List bookmarks | TWITTER_BOOKMARKS_BY_USER | id |
| Add bookmark | TWITTER_ADD_POST_TO_BOOKMARKS | tweet_id |
| Remove bookmark | TWITTER_REMOVE_A_BOOKMARKED_POST | tweet_id |
| Unlike post | TWITTER_UNLIKE_POST | tweet_id |
| Liked posts | TWITTER_RETURNS_POST_OBJECTS_LIKED_BY_THE_PROVIDED_USER_ID | id |
| Owned lists | TWITTER_GET_A_USER_S_OWNED_LISTS | id |
| List memberships | TWITTER_GET_A_USER_S_LIST_MEMBERSHIPS | id |
| Pinned lists | TWITTER_GET_A_USER_S_PINNED_LISTS | id |
| Followed lists | TWITTER_GET_USER_S_FOLLOWED_LISTS | id |
| List details | TWITTER_LIST_LOOKUP_BY_LIST_ID | list_id |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.
