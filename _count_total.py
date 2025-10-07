import os, time, sys, requests
API_URL = 'https://api.fireflies.ai/graphql'
TOKEN = os.getenv('FIREFLIES_TOKEN')
if not TOKEN:
    print('TOKEN_MISSING')
    sys.exit(1)
headers = {'Authorization': f'Bearer {TOKEN}'}
query = '''
query ($skip:Int!, $limit:Int!){
  transcripts(skip:$skip, limit:$limit){ id }
}
'''
count = 0
skip = 0
PAGE_SIZE = 50
retries = 4
while True:
    for attempt in range(retries):
        try:
            r = requests.post(API_URL, json={'query': query, 'variables': {'skip': skip, 'limit': PAGE_SIZE}}, headers=headers, timeout=60)
            r.raise_for_status()
            j = r.json()
            if 'errors' in j:
                raise RuntimeError(j['errors'])
            batch = j['data']['transcripts']
            break
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(1.0 * (attempt + 1))
    if not batch:
        break
    count += len(batch)
    skip += PAGE_SIZE
    time.sleep(0.1)
print(count)
