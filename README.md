# **Instructions to run**
1. Clone repository
1. Install requirements.txt using  
`pip install -r requirements.txt`
1. Create file 'config.py'
2. Add the following fields:  

    firebase_key_path = "path-to-firebase-json"  
    tbo_base_url = "tbo api base url"  
    user_name = "user name for tbo api"  
    password = "password for tbo api"  
    api_key="google generative ai key"
3. run using  
`python -m uvicorn main:app --reload --host {insert ip here}`