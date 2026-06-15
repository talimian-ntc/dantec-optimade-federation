import requests


#  ---------------------------------------------------------------------------------------------------------------------
#  Functions
#  ---------------------------------------------------------------------------------------------------------------------
class RavenDBClient:
    def __init__(self, base_url, database):
        self.base_url = base_url
        self.database = database
        self.query_url = f"{self.base_url}/databases/{self.database}/queries"
        self.docs_url = f"{self.base_url}/databases/{self.database}/docs"
        self.headers = {"Accept-Encoding": "identity"}

    def query(self, query_string):
        payload = {"Query": query_string}
        response = requests.post(self.query_url, json=payload, headers=self.headers)

        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                print("Response is not valid JSON")
                return None
        else:
            print(f"Request failed with status code {response.status_code}")
            return None

    # -------------------------------------------------------------------------------------------------
    # Get document by ID
    # -------------------------------------------------------------------------------------------------
    def get_document(self, doc_id):
        params = {"id": doc_id}
        response = requests.get(self.docs_url, params=params, headers=self.headers)

        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                print("Response is not valid JSON")
                return None
        elif response.status_code == 404:
            print("Document not found")
            return None
        else:
            print(f"Request failed with status code {response.status_code}")
            return None

    # -------------------------------------------------------------------------------------------------
    # Insert (or update) single document
    # -------------------------------------------------------------------------------------------------

    def insert_single_document(self, data):

        params = {'id': data['id']}

        material_data = {'title': data['title'],
                         'date': data['date'],
                         'formula': data['formula'],
                         'elements': data['elements'],
                         'authors': data['authors']}

        response = requests.put(self.docs_url, params=params, json=material_data, headers=self.headers)

        if response.status_code in (200, 201):
            try:
                response.json()
            except ValueError:
                print("Response is not valid JSON")
        else:
            print(f"Insert failed with status code {response.status_code}")

        return

    # -------------------------------------------------------------------------------------------------
    # Insert (or update) document
    # -------------------------------------------------------------------------------------------------
    def insert_document(self, data):

        for item in data:

            params = {'id': item['id']}

            material_data = {'title': item['title'],
                             'date': item['date'],
                             'formula': item['formula'],
                             'elements': item['elements'],
                             'authors': item['authors']}

            response = requests.put(self.docs_url, params=params, json=material_data, headers=self.headers)

            if response.status_code in (200, 201):
                try:
                    response.json()
                except ValueError:
                    print("Response is not valid JSON")
            else:
                print(f"Insert failed with status code {response.status_code}")
        return

    # -------------------------------------------------------------------------------------------------
    # Delete document
    # -------------------------------------------------------------------------------------------------
    def delete_document(self, doc_id):
        params = {"id": doc_id}
        response = requests.delete(self.docs_url, params=params, headers=self.headers)

        if response.status_code == 204:
            print("Document deleted successfully")
            return True
        elif response.status_code == 404:
            print("Document not found")
            return False
        else:
            print(f"Delete failed with status code {response.status_code}")
            return False
