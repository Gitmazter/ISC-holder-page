const API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE2Nzk0MDYyOTMzNzksImVtYWlsIjoicGhpbGlwLmFuZGVsaWNAZ21haWwuY29tIiwiYWN0aW9uIjoidG9rZW4tYXBpIiwiaWF0IjoxNjc5NDA2MjkzfQ.tXTxsQtNuozzX5OCdGLfIMaqH-KdVQJjAtfKq91ReDs";

export const fetchISCMeta = async () => {
    //console.log("fetching meta....");
    const API_URL = 'https://public-api.solscan.io/token/meta?tokenAddress=J9BcrQfX4p9D1bvLzRNCbMDv8f44a9LFdeqNE4Yk2WMD'
    const CONFIG = {
        headers: {
            "token":API_KEY
        }
    }  
    const meta = await fetch(API_URL, CONFIG)
    .then((res) => res.json())
    .then((data) => {return data})
    return meta;
}

export const fetchISCHolders = async () => {
    const API_URL = "https://public-api.solscan.io/token/holders?tokenAddress=J9BcrQfX4p9D1bvLzRNCbMDv8f44a9LFdeqNE4Yk2WMD&limit=26&offset=0";
    const CONFIG = {
        headers: {
            "token":API_KEY
        }
    }  
    const data = await fetch(API_URL, CONFIG)
    .then((res) => res.json())
    .then((data) => {return data})

    return data;
}