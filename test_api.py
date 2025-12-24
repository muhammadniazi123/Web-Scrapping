import requests
import json

API_BASE_URL = "http://localhost:5000"

def test_health():
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_search_get():
    print("\nTesting /search endpoint (GET)...")
    try:
        query = "machine learning"
        response = requests.get(f"{API_BASE_URL}/search", params={"query": query, "top_n": 5})
        print(f"Status Code: {response.status_code}")
        print(f"Query: {query}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_search_post():
    print("\nTesting /search endpoint (POST)...")
    try:
        data = {
            "query": "data science",
            "top_n": 10
        }
        response = requests.post(f"{API_BASE_URL}/search", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Request Data: {json.dumps(data, indent=2)}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_documentation():
    print("\nTesting / endpoint (documentation)...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    print("="*60)
    print("Medium Search API Test Suite")
    print("="*60)
    
    import sys
    if len(sys.argv) > 1:
        API_BASE_URL = sys.argv[1]
        print(f"Using API URL: {API_BASE_URL}")
    
    results = []
    results.append(("Health Check", test_health()))
    results.append(("Documentation", test_documentation()))
    results.append(("Search (GET)", test_search_get()))
    results.append(("Search (POST)", test_search_post()))
    
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    print(f"\nOverall: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'}")
