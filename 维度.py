raw = [
    [
        "https://cdn.customily.com/shopify/assetFiles/previews/wdp-us.myshopify.com/fe5d28f4-2197-48b8-b596-0280329d3392.jpeg"
    ],
    [
        "https://cdn.customily.com/shopify/assetFiles/previews/wdp-us.myshopify.com/fe5d28f4-2197-48b8-b596-0280329d3392.jpeg"
    ],
    [
        "https://cdn.customily.com/shopify/assetFiles/previews/wdp-us.myshopify.com/fe5d28f4-2197-48b8-b596-0280329d3392.jpeg"
    ],
]

import re

# 正则提取 https?://... 形式的链接
links = [m for item in raw for m in re.findall(r'https?://[^\s<>"\']+', str(item))]
print(links)
