"""REST client handling, including TalonOneStream base class."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Iterable

import requests
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseOffsetPaginator  # noqa: TCH002
from singer_sdk.streams import RESTStream

from tap_talonone.pagination import Paginator

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]


class TalonOneStream(RESTStream):
    """TalonOne stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config['api_url']

    records_jsonpath = "$.data[*]"  # Or override `parse_response`.

    # Set this value or override `get_new_paginator`.
    next_page_token_jsonpath = "$.next_page"  # noqa: S105

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="Authorization",
            value="ManagementKey-v1 " + self.config.get("auth_token", ""),
            location="header"
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        return headers

    def get_new_paginator(self) -> BaseOffsetPaginator:
        return Paginator(start_value=0, page_size=self.config["page_size"])

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        params: dict = {
            "skip": 0,
            "pageSize": self.config["page_size"]
        }
        if next_page_token:
            params["skip"] = next_page_token
        return params
