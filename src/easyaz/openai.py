import logging
import typing

if typing.TYPE_CHECKING:
    from azure.core.credentials import TokenCredential

import openai.api_requestor

from . import core

log = logging.getLogger(__name__)

def login(
    endpoint: str, credential: "TokenCredential", *, api_version: str | None = None
) -> None:
    if openai.api_version and api_version:
        log.info(f'Overriding openai.api_version "{openai.api_version}" with api_version "{api_version}" passed to easyaz.openai.login') 
    openai.api_version = api_version or openai.api_version or '2022-12-01'
    
    if openai.api_base and endpoint != openai.api_base:
        log.info(f'Overriding openai.endpoint "{openai.api_base}" with endpoint "{endpoint}" passed to easyaz.openai.login')
    openai.api_base = endpoint
    
    openai.api_key = core.AZUREAD_FAKE_API_KEY
    openai.api_type = "azuread"

    wrapped = getattr(openai.api_requestor, "_make_session")

    def factory():
        session = wrapped()
        session.mount(
            endpoint,
            core.AzHttpAdapter(
                credential=credential,
                scopes="https://cognitiveservices.azure.com/.default",
                max_retries=2,
            ),
        )
        return session

    # Monkey-patching internal methods is not the greatest thing in the world
    # We'll open a PR to openai-path that allow apps to provide a session factory for 
    # requests in the same way it does for aiohttp.... But for now....
    setattr(openai.api_requestor, "_make_session", factory)
