"""TalonOne tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_talonone import streams


class TapTalonOne(Tap):
    """TalonOne tap class."""

    name = "tap-talonone"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=True,
            secret=True,
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
        th.Property(
            "api_url",
            th.StringType,
            required=True,
            description="The base URL for your Talon One account",
        ),
        th.Property(
            "account_id",
            th.IntegerType,
            required=True,
            description="The ID for your account",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.TalonOneStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.UsersStream(self),
            streams.AccountsStream(self),
            streams.AccountAnalyticsStream(self),
            streams.ApplicationsStream(self),
            streams.CampaignsStream(self),
            streams.CouponsStream(self),
            streams.ChangesStream(self),
        ]


if __name__ == "__main__":
    TapTalonOne.cli()
