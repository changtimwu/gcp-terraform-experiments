from google.oauth2 import service_account
import google.auth.transport.requests


def get_idToken_from_serviceaccount(json_credential_path: str, target_audience: str):
    """
    TODO(Developer): Replace the below variables before running the code.

    *NOTE*:
    Using service account keys introduces risk; they are long-lived, and can be used by anyone
    that obtains the key. Proper rotation and storage reduce this risk but do not eliminate it.
    For these reasons, you should consider an alternative approach that
    does not use a service account key. Several alternatives to service account keys
    are described here:
    https://cloud.google.com/docs/authentication/external/set-up-adc

    Args:
        json_credential_path: Path to the service account json credential file.
        target_audience: The url or target audience to obtain the ID token for.
                        Examples: http://www.abc.com
    """
    # Obtain the id token by providing the json file path and target audience.
    credentials = service_account.IDTokenCredentials.from_service_account_file(
        filename=json_credential_path,
        target_audience=target_audience)
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    print("Generated ID token.")
    print(credentials.token)
    print(request.session)
    

#check create_sa_key.sh 
cred='sakey.json'
get_idToken_from_serviceaccount( cred, 'https://private-service-7ahpw2de5a-de.a.run.app')
 
