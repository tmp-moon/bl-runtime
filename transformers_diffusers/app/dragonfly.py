import requests
from requests.adapters import HTTPAdapter
from typing import Optional

DRAGONFLY_URL: Optional[str] = None


def set_dragonfly_url(url: str):
    global DRAGONFLY_URL
    DRAGONFLY_URL = url


class DragonflyAdapter(HTTPAdapter):
    def get_connection_with_tls_context(
        self,
        request: requests.Request,
        verify: bool,
        proxies: Optional[dict],
        cert: Optional[str],
    ) -> requests.Session:
        if "repos" in request.url:  ## Depends on the config of the dragonfly server
            request.url = request.url.replace("https://", "http://")
        return super().get_connection_with_tls_context(request, verify, proxies, cert)


# Create a factory function that returns a new Session.
def backend_factory() -> requests.Session:
    session = requests.Session()
    session.mount("http://", DragonflyAdapter())
    session.mount("https://", DragonflyAdapter())
    session.proxies = {
        "https": DRAGONFLY_URL,
        "http": DRAGONFLY_URL,
    }
    session.verify = False
    return session
