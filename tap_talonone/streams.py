"""Stream type classes for tap-talonone."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.helpers._typing import TypeConformanceLevel

from tap_talonone.client import TalonOneStream


class UsersStream(TalonOneStream):
    name = "users"
    path = "/v1/users"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("created", th.DateTimeType),
        th.Property("modified", th.DateTimeType),
        th.Property("email", th.StringType),
        th.Property("accountId", th.IntegerType),
        th.Property("state", th.StringType),
        th.Property("name", th.StringType),
        th.Property("latestFeedTimestamp", th.DateTimeType),
        th.Property("roles", th.ArrayType(th.IntegerType)),
        th.Property("authMethod", th.StringType),
    ).to_dict()


class AccountsStream(TalonOneStream):

    name = "accounts"
    path = "/v1/accounts/{account_id}"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("created", th.DateTimeType),
        th.Property("modified", th.DateTimeType),
        th.Property("companyName", th.StringType),
        th.Property("domainName", th.StringType),
        th.Property("state", th.StringType),
        th.Property("billingEmail", th.StringType),
        th.Property("planName", th.StringType),
        th.Property("planExpires", th.DateTimeType),
        th.Property("applicationLimit", th.IntegerType),
        th.Property("userLimit", th.IntegerType),
        th.Property("campaignLimit", th.IntegerType),
        th.Property("apiLimit", th.IntegerType),
        th.Property("applicationCount", th.IntegerType),
        th.Property("userCount", th.IntegerType),
        th.Property("campaignsActiveCount", th.IntegerType),
        th.Property("campaignsInactiveCount", th.IntegerType),
    ).to_dict()


class AccountAnalyticsStream(TalonOneStream):
    name = "account_analytics"
    path = "/v1/accounts/{account_id}/analytics"
    primary_keys = ["account_id"]
    replication_key = None
    records_jsonpath = "$"
    schema = th.PropertiesList(
        th.Property("account_id", th.IntegerType),
        th.Property("applications", th.IntegerType),
        th.Property("liveApplications", th.IntegerType),
        th.Property("sandboxApplications", th.IntegerType),
        th.Property("campaigns", th.IntegerType),
        th.Property("activeCampaigns", th.IntegerType),
        th.Property("liveActiveCampaigns", th.IntegerType),
        th.Property("coupons", th.IntegerType),
        th.Property("activeCoupons", th.IntegerType),
        th.Property("expiredCoupons", th.IntegerType),
        th.Property("referralCodes", th.IntegerType),
        th.Property("activeReferralCodes", th.IntegerType),
        th.Property("expiredReferralCodes", th.IntegerType),
        th.Property("activeRules", th.IntegerType),
        th.Property("users", th.IntegerType),
        th.Property("roles", th.IntegerType),
        th.Property("customAttributes", th.IntegerType),
        th.Property("webhooks", th.IntegerType),
        th.Property("loyaltyPrograms", th.IntegerType),
        th.Property("liveLoyaltyPrograms", th.IntegerType),
    ).to_dict()

    def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
        row["account_id"] = self.config["account_id"]
        return row


class ApplicationsStream(TalonOneStream):
    name = "applications"
    path = "/v1/applications"
    primary_keys = ["id"]
    replication_key = None
    TYPE_CONFORMANCE_LEVEL = TypeConformanceLevel.ROOT_ONLY
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("created", th.DateTimeType),
        th.Property("modified", th.DateTimeType),
        th.Property("accountId", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("timezone", th.StringType),
        th.Property("currency", th.StringType),
        th.Property("caseSensitivity", th.StringType),
        th.Property("attributes", th.ObjectType()),
        th.Property("limits", th.ArrayType(th.ObjectType(
            th.Property("action", th.StringType),
            th.Property("limit", th.IntegerType),
            th.Property("period", th.StringType),
            th.Property("entities", th.ArrayType(th.StringType)),
        ))),
        th.Property("enableCascadingDiscounts", th.BooleanType),
        th.Property("attributesSettings", th.ObjectType(
            th.Property("mandatory", th.ObjectType(
                th.Property("campaigns", th.ArrayType(th.StringType)),
                th.Property("coupons", th.ArrayType(th.StringType)),
            )),
        )),
        th.Property("enableCascadingDiscounts", th.BooleanType),
        th.Property("enablePartialDiscounts", th.BooleanType),
        th.Property("loyaltyPrograms", th.ArrayType(
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("created", th.DateTimeType),
                th.Property("title", th.StringType),
                th.Property("description", th.StringType),
                th.Property("subscribedApplications", th.ArrayType(th.IntegerType)),
                th.Property("defaultValidity", th.StringType),
                th.Property("defaultPending", th.StringType),
                th.Property("allowSubledger", th.BooleanType),
                th.Property("sandbox", th.BooleanType),
                th.Property("accountID", th.IntegerType),
                th.Property("name", th.StringType),
                th.Property("tiers", th.ArrayType(th.StringType)),
                th.Property("timezone", th.StringType),
                th.Property("cardBased", th.BooleanType),
            ),
        )),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "application_id": record["id"]
        }


class CampaignsStream(TalonOneStream):
    name = "campaigns"
    path = "/v1/applications/{application_id}/campaigns"
    primary_keys = ["id"]
    replication_key = None
    parent_stream_type = ApplicationsStream
    ignore_parent_replication_keys = True
    TYPE_CONFORMANCE_LEVEL = TypeConformanceLevel.ROOT_ONLY
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("created", th.DateTimeType),
        th.Property("applicationId", th.IntegerType),
        th.Property("userId", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("startTime", th.DateTimeType),
        th.Property("endTime", th.DateTimeType),
        th.Property("attributes", th.ObjectType()),
        th.Property("state", th.StringType),
        th.Property("activeRulesetId", th.IntegerType),
        th.Property("tags", th.ArrayType(th.StringType)),
        th.Property("features", th.ArrayType(th.StringType)),
        th.Property("couponSettings", th.ObjectType(
            th.Property("validCharacters", th.ArrayType(th.StringType)),
            th.Property("couponPattern", th.StringType),
        )),
        th.Property("limits", th.ArrayType(th.ObjectType(
            th.Property("action", th.StringType),
            th.Property("limit", th.IntegerType),
            th.Property("period", th.StringType),
            th.Property("entities", th.ArrayType(th.StringType)),
        ))),
        th.Property("campaignGroups", th.ArrayType(th.IntegerType)),
        th.Property("couponRedemptionCount", th.IntegerType),
        th.Property("discountCount", th.IntegerType),
        th.Property("discountEffectCount", th.IntegerType),
        th.Property("couponCreationCount", th.IntegerType),
        th.Property("customEffectCount", th.IntegerType),
        th.Property("addFreeItemEffectCount", th.IntegerType),
        th.Property("callApiEffectCount", th.IntegerType),
        th.Property("reservecouponEffectCount", th.IntegerType),
        th.Property("updated", th.DateTimeType),
        th.Property("updatedBy", th.StringType),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "application_id": context["application_id"],
            "campaign_id": record["id"]
        }


class CouponsStream(TalonOneStream):
    name = "coupons"
    path = "/v1/applications/{application_id}/campaigns/{campaign_id}/coupons/no_total"
    primary_keys = ["id"]
    replication_key = None
    parent_stream_type = CampaignsStream
    ignore_parent_replication_keys = True
    TYPE_CONFORMANCE_LEVEL = TypeConformanceLevel.ROOT_ONLY
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("created", th.DateTimeType),
        th.Property("campaignId", th.IntegerType),
        th.Property("value", th.StringType),
        th.Property("usageLimit", th.IntegerType),
        th.Property("discountLimit", th.IntegerType),
        th.Property("reservationLimit", th.IntegerType),
        th.Property("startDate", th.DateTimeType),
        th.Property("expiryDate", th.DateTimeType),
        th.Property("limits", th.ArrayType(th.ObjectType(
            th.Property("action", th.StringType),
            th.Property("limit", th.IntegerType),
            th.Property("period", th.StringType),
            th.Property("entities", th.ArrayType(th.StringType)),
        ))),
        th.Property("usageCounter", th.IntegerType),
        th.Property("discountCounter", th.IntegerType),
        th.Property("discountRemainder", th.IntegerType),
        th.Property("reservationCounter", th.IntegerType),
        th.Property("attributes", th.ObjectType()),
        th.Property("referralId", th.IntegerType),
        th.Property("recipientIntegrationId", th.StringType),
        th.Property("importId", th.IntegerType),
        th.Property("reservation", th.BooleanType),
        th.Property("batchId", th.StringType),
        th.Property("isReservationMandatory", th.BooleanType),
    ).to_dict()


class ChangesStream(TalonOneStream):
    name = "changes"
    path = "/v1/changes"
    primary_keys = ["id"]
    replication_key = "created"
    TYPE_CONFORMANCE_LEVEL = TypeConformanceLevel.ROOT_ONLY
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("created", th.DateTimeType),
        th.Property("userId", th.IntegerType),
        th.Property("managementKeyId", th.IntegerType),
        th.Property("applicationId", th.IntegerType),
        th.Property("entity", th.StringType),
        th.Property("old", th.ObjectType()),
        th.Property("new", th.ObjectType()),
    ).to_dict()

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        params: dict = {
            "skip": 0
        }
        if next_page_token:
            params["skip"] = next_page_token
        if self.replication_key:
            start_date = self.get_starting_timestamp(context)
            start_date_formatted = start_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            params["createdAfter"] = start_date_formatted
        return params

class AdditionalCostsStream(TalonOneStream):
    name = "additional_costs"
    path = "/v1/additional_costs"
    primary_keys = ["id"]
    replication_key = "created"
    TYPE_CONFORMANCE_LEVEL = TypeConformanceLevel.ROOT_ONLY
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("created", th.DateTimeType),
        th.Property("accountId", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("title", th.StringType),
        th.Property("description", th.StringType),
        th.Property("subscribedApplicationsIds", th.ArrayType(th.IntegerType)),
        th.Property("type", th.StringType),
    ).to_dict()

class ReferralsStream(TalonOneStream):
    name = "referrals"
    path = "/v1/applications/{application_id}/campaigns/{campaign_id}/referrals/no_total"
    primary_keys = ["id"]
    replication_key = "created"
    parent_stream_type = CampaignsStream
    ignore_parent_replication_keys = True
    TYPE_CONFORMANCE_LEVEL = TypeConformanceLevel.ROOT_ONLY
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("created", th.DateTimeType),
        th.Property("startDate", th.DateTimeType),
        th.Property("expirtDate", th.DateTimeType),
        th.Property("usageLimit", th.IntegerType),
        th.Property("campaignId", th.IntegerType),
        th.Property("advocateProfileIntegrationId", th.StringType),
        th.Property("friendProfileIntegrationId", th.StringType),
        th.Property("attributes", th.ArrayType(th.StringType)),
        th.Property("importId", th.IntegerType),
        th.Property("code", th.StringType),
        th.Property("usageCounter", th.IntegerType),
        th.Property("batchId", th.StringType),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "application_id": context["application_id"],
            "integration_id": record["advocateProfileIntegrationId"]
        }

class FriendsStream(TalonOneStream):
    name = "friends"
    path = "/v1/applications/{application_id}/profile/{integration_id}/friends"
    primary_keys = ["sessionId"]
    replication_key = "created"
    parent_stream_type = ReferralsStream
    ignore_parent_replication_keys = True
    TYPE_CONFORMANCE_LEVEL = TypeConformanceLevel.ROOT_ONLY
    schema = th.PropertiesList(
        th.Property("applicationId", th.IntegerType),
        th.Property("sessionId", th.StringType),
        th.Property("advocateIntegrationId", th.StringType),
        th.Property("friendIntegrationId", th.StringType),
        th.Property("code", th.StringType),
        th.Property("created", th.DateTimeType),
    ).to_dict()
