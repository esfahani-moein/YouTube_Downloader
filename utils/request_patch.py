import pytubefix.request

def apply_request_patch():
    # Store the original request function
    original_request = pytubefix.request._execute_request
    
    # Create a patched version with browser-like headers
    def patched_request(url, method=None, headers=None, data=None, timeout=30):
        if headers is None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Referer': 'https://www.youtube.com/'
            }
        return original_request(url, method=method, headers=headers, data=data, timeout=timeout)
    
    # Replace the original with our patched version
    pytubefix.request._execute_request = patched_request
    print("Applied YouTube download workaround")