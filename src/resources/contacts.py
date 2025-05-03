
from utils.api import zoho_api_request


def list_contacts(page: int = 1, per_page: int = 100, sort_column: str = "contact_name", query_params: dict[str, str] = None) -> dict[str, any]:
    """
    List all contacts in the Zoho Inventory account.

    Args:
        page (int): The page number to retrieve for pagination.
        per_page (int): The number of contacts per page.
        sort_column (str): The column to sort by(contact_name, created_time, last_modified_time).
        query_params (dict[str, str], optional): Additional query parameters for filtering contacts.
            Accepted keys include:
                - 'contact_name': Search contacts by contact name. Maximum length [100] 
                - 'company_name': Search contacts by company name. Maximum length [100] 
                - 'email': search contacts by email. Maximum length [100]
                - 'search_text': Search contacts by contact name or notes. Maximum length [100]  
                - 'phone': search contacts by phone. Maximum length [100]
                - 'first_name': search contacts by first name. Maximum length [100]
                - 'last_name': search contacts by last name. Maximum length [100]

    Returns:
        dict[str, any]: A dictionary containing the list of contacts and pagination information.
    """
    params = {
            "page": page,
            "per_page": per_page,
            "sort_column": sort_column,
        }

    #validate query params 
    if query_params:
        if 'contact_name' in query_params:
            if len(query_params['contact_name']) > 100:
                raise ValueError("contact_name exceeds maximum length of 100 characters")
            else:
                params['contact_name_contains'] = query_params['contact_name']
        if 'company_name' in query_params:
            if len(query_params['company_name']) > 100:
                raise ValueError("company_name exceeds maximum length of 100 characters")
            else:
                params['company_name_contains'] = query_params['company_name']
        if 'email' in query_params:
            if len(query_params['email']) > 100:
                raise ValueError("email exceeds maximum length of 100 characters")
            else:
                params['email_contains'] = query_params['email']
        if 'search_text' in query_params:
            if len(query_params['search_text']) > 100:
                raise ValueError("search_text exceeds maximum length of 100 characters")
            else:
                params['search_text'] = query_params['search_text']
        if 'phone' in query_params:
            if len(query_params['phone']) > 100:
                raise ValueError("phone exceeds maximum length of 100 characters")
            else:
                params['phone_contains'] = query_params['phone']
        if 'first_name' in query_params:
            if len(query_params['first_name']) > 100:
                raise ValueError("first_name exceeds maximum length of 100 characters")
            else:
                params['first_name_contains'] = query_params['first_name']
        if 'last_name' in query_params: 
            if len(query_params['last_name']) > 100:
                raise ValueError("last_name exceeds maximum length of 100 characters")
            else:
                params['last_name_contains'] = query_params['last_name']

    try:
        response= zoho_api_request('GET', '/contacts', params=params)
        result = {
            "page": page,
            "per_page": per_page,
            "has_more_page": response.get("page_context", {}).get("has_more_page", False),
            "contacts": response.get("contacts", []),
            "message": response.get("message", ""),
        }
        if "page_context" in response and "total" in response["page_context"]:
            result["total"] = response["page_context"]["total"]
        return result
    except Exception as e:
        print(f"Error listing contacts: {e}")
        return None

def get_contact(contact_id: str) -> dict[str, any]:
    """
    Get detailed info about a specific contact with the id. 

    Args:
        contact_id (str): The ID of the contact to retrieve.

    Returns:
        dict[str, any]: A dictionary containing the contact details.
    """

    if not isinstance(contact_id, str):
        raise TypeError("contact_id must be a string")
    try:
       respone = zoho_api_request('GET', f'/contacts/{contact_id}')

       if not respone.get('contact'):
           raise ValueError("Contact not found")
       else:
           result ={
            'contact': respone.get('contact'),
            'message': respone.get('message', ''),
           }
           return result
    except Exception as e:
        print(f"Error getting contact: {e}")
        return None