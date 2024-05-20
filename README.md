# cachemoney

Extracts files from Chrome/Chromium/Electron cache.

## usage

Requires Python 3.6+ (probably).

This will extract all files whose original URL ended with JPG into `files/`.

```
python -m cachemoney --cache-dir /Users/me/Chrome/Cache --output-root files --filter '*jpg'
```

### Chrome on MacOS

```
python -m cachemoney --cache-dir ~/Library/Caches/Google/Chrome/Default/Cache/Cache_Data --output-root files --filter '*jpg'
```

## cache-dir

### MacOS

#### Chrome
```shell
~/Library/Caches/Google/Chrome/Default/Cache/Cache_Data
```